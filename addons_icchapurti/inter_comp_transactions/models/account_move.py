# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    related_so = fields.Many2one('sale.order', string="Related Sale Order")
    counterpart_po = fields.Char(string="Purchase Order")

    def action_post(self):
        res = super(AccountMove, self).action_post()
        if self.related_so:
            trans_enabled = self.env['ir.config_parameter'].sudo().get_param(
                'inter_comp_transactions.sale_purchase_sync')
            auto_validate = self.env['ir.config_parameter'].sudo().get_param(
                'inter_comp_transactions.auto_validate')
            if trans_enabled:
                order_lines = []
                company_id = self.env['res.company'].sudo().search(
                    [('partner_id', '=', self.related_so.partner_id.id)])

                for item in self.invoice_line_ids:
                    taxes = []
                    for tax in item.tax_ids:
                        tax_id = self.env['account.tax'].sudo().search(
                            [('name', '=', tax.name),
                             ('company_id', '=', company_id.id)], limit=1)
                        if tax_id:
                            taxes.append(tax_id.id)
                    order_line = (0, 0, {
                        'name': item.name,
                        'product_id': item.product_id.id,
                        'product_qty': item.quantity,
                        'product_uom': item.product_uom_id.id,
                        'price_unit': item.price_unit,
                        'taxes_id': taxes,
                    })
                    order_lines.append(order_line)

                company_id = self.env['res.company'].sudo().search(
                    [('partner_id', '=', self.related_so.partner_id.id)])
                if company_id:
                    picking_type_id = self.env[
                        'stock.picking.type'].sudo().search(
                        [('code', '=', 'incoming'),
                         ('warehouse_id.company_id', '=', company_id.id)],
                        limit=1)
                    gst_treatment = self.env.company.partner_id.l10n_in_gst_treatment

                    purchase_order = self.env['purchase.order'].sudo().create({
                        'partner_id': self.env.company.partner_id.id,
                        'partner_ref': self.related_so.name,
                        'order_line': order_lines,
                        'picking_type_id': picking_type_id.id,
                        'l10n_in_gst_treatment': gst_treatment,
                        'sync_order': True,
                        'counterpart_so': self.related_so.name,
                        'counterpart_invoice': self.name
                    })
                    picking_type_id = self.env[
                        'stock.picking.type'].sudo().search(
                        [('code', '=', 'incoming'),
                         ('warehouse_id.company_id', '=', company_id.id)],
                        limit=1)
                    purchase_order.write({
                        'company_id': company_id.id,
                        'picking_type_id': picking_type_id.id
                    })
                    self.counterpart_po = purchase_order.name
                    if auto_validate:
                        try:
                            purchase_order.sudo().button_confirm()
                        except ValueError:
                            return res
        return res
