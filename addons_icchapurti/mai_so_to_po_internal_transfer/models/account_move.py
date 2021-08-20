# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    move_id = fields.Many2one('account.move', string='Invoice', readonly=True, copy=False)


class AccountMove(models.Model):
    _inherit = "account.move"

    purchase_order_id = fields.Many2one('purchase.order',
                                        string='Purchase Order',
                                        readonly=True, copy=False)

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        sale_order_id = self.env['sale.order'].search([('name', '=', res.invoice_origin)])
        if sale_order_id and sale_order_id.company_id.po_option == 'invoice':
            company_obj = self.env['res.company']
            purchase_order_obj = self.env['purchase.order']
            purchase_line_obj = self.env['purchase.order.line']
            purchase_vals = res._prepare_purchase_order(sale_order_id.company_id, sale_order_id.company_id.po_company_id)
            purchase_id = purchase_order_obj.sudo().create(purchase_vals)
            for line in res.invoice_line_ids:
                line_vals = line._prepare_purchase_order_line(purchase_id, sale_order_id.company_id.po_company_id)
                purchase_line_obj.sudo().create(line_vals)
            res.purchase_order_id = purchase_id.id
        return res

    def _prepare_purchase_order(self, main_company, company):
        res = {
            'name': self.env['ir.sequence'].sudo().next_by_code(
                'purchase.order'),
            'origin': self.name,
            'partner_ref': self.name,
            'partner_id': main_company.partner_id.id,
            'dest_address_id': main_company.partner_id.id,
            'date_order': self.invoice_date or self.create_date,
            'company_id': company.id,
            'payment_term_id': self.invoice_payment_term_id.id,
            'fiscal_position_id': self.fiscal_position_id.id,
            'move_id': self.id,
        }
        return res


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _prepare_purchase_order_line(self, purchase_id, company):
        price_unit = self.price_unit
        if self.discount:
            price_unit = self.price_unit - (self.price_unit * (
                self.discount / 100))
        line_taxes = self.tax_ids
        if self.product_id.supplier_taxes_id:
            line_taxes = \
                self.product_id.sudo().supplier_taxes_id

        res = {
            'name': self.name or '',
            'product_id': self.product_id.id,
            'product_uom': self.product_id.uom_po_id.id or
            self.product_uom.id,
            'product_qty': self.quantity,
            'price_unit': price_unit,
            'taxes_id': [(6, 0, [
                sales_tax.id for sales_tax in line_taxes
                if sales_tax.company_id.id == company.id])],
            'date_planned': purchase_id.date_planned or
            purchase_id.date_order or False,
            'company_id': company.id,
            'order_id': purchase_id.id,
        }
        return res
