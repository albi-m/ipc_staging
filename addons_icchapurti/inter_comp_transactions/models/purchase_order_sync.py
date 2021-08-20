# -*- coding: utf-8 -*-

from odoo import models, fields


class PurchaseOrderSync(models.Model):
    """
    Generate a draft sales order when a company confirms a purchase order
    for the current company
    """
    _inherit = 'purchase.order'

    sync_order = fields.Boolean(default=False)
    l10n_in_gst_treatment = fields.Selection(states={
        'purchase': [('readonly', False)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    })
    counterpart_so = fields.Char(string="Sale Order Reference")
    counterpart_invoice = fields.Char(string="Invoice Reference")

    '''
    Currently disabled as it only requires Sale order synchronisation
    '''
    # def button_confirm(self):
    #     res = super(PurchaseOrderSync, self).button_confirm()
    #     if not self.sync_order:
    #         trans_enabled = self.env['ir.config_parameter'].sudo().get_param(
    #             'inter_comp_transactions.sale_purchase_sync')
    #         auto_validate = self.env['ir.config_parameter'].sudo().get_param(
    #             'inter_comp_transactions.auto_validate')
    #         if trans_enabled:
    #             if self.partner_id.company_type == 'company':
    #                 company_id = self.env['res.company'].sudo().search(
    #                     [('partner_id', '=', self.partner_id.id)])
    #                 order_lines = []
    #                 for item in self.order_line:
    #                     taxes = []
    #                     for tax in item.taxes_id:
    #                         tax_id = self.env['account.tax'].sudo().search(
    #                             [('name', '=', tax.name),
    #                              ('company_id', '=', company_id.id)], limit=1)
    #                         if tax_id:
    #                             taxes.append(tax_id.id)
    #                     order_line = (0, 0, {
    #                         'name': item.name,
    #                         'product_id': item.product_id.id,
    #                         'product_uom_qty': item.product_qty,
    #                         'product_uom': item.product_uom.id,
    #                         'price_unit': item.price_unit,
    #                         'tax_id': taxes
    #                     })
    #                     print("UoM : ", item.product_uom.name)
    #                     order_lines.append(order_line)
    #                 company_id = self.env['res.company'].sudo().search(
    #                     [('partner_id', '=', self.partner_id.id)])
    #                 if company_id:
    #                     sale_order = self.env['sale.order'].sudo().create({
    #                         'partner_id': self.env.company.partner_id.id,
    #                         'order_line': order_lines,
    #                         'company_id': company_id.id,
    #                         'sync_order': True
    #                     })
    #                     if auto_validate:
    #                         sale_order.sudo().action_confirm()
    #         return res
