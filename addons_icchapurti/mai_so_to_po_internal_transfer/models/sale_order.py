# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    sale_order_id = fields.Many2one('sale.order',
                                    string='Sale Order', readonly=True,
                                    copy=False)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    purchase_order_id = fields.Many2one('purchase.order',
                                        string='Purchase Order',
                                        readonly=True, copy=False)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.company_id.po_option == 'sale':
            company_obj = self.env['res.company']
            purchase_order_obj = self.env['purchase.order']
            purchase_line_obj = self.env['purchase.order.line']
            purchase_vals = self._prepare_purchase_order(self.company_id.po_company_id)
            purchase_id = purchase_order_obj.sudo().create(purchase_vals)
            for line in self.order_line:
                line_vals = line._prepare_purchase_order_line(purchase_id, self.company_id.po_company_id)
                purchase_line_obj.sudo().create(line_vals)
            purchase_id.with_context(company=self.company_id.po_company_id.id).sudo().button_confirm()
        return res

    def _prepare_purchase_order(self, company):
        res = {
            'name': self.env['ir.sequence'].sudo().with_context(company=company.id).next_by_code(
                'purchase.order'),
            'origin': self.name,
            'partner_ref': self.name,
            'partner_id': self.company_id.partner_id.id,
            'dest_address_id': self.company_id.partner_id.id,
            'date_order': self.date_order,
            'company_id': company.id,
            'payment_term_id': self.payment_term_id.id,
            'fiscal_position_id': self.fiscal_position_id.id,
            'sale_order_id': self.id,
        }
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_purchase_order_line(self, purchase_id, company):
        price_unit = self.price_unit
        if self.discount:
            price_unit = self.price_unit - (self.price_unit * (
                self.discount / 100))
        line_taxes = self.tax_id
        if self.product_id.supplier_taxes_id:
            line_taxes = \
                self.product_id.sudo().supplier_taxes_id

        res = {
            'name': self.name or '',
            'product_id': self.product_id.id,
            'product_uom': self.product_id.uom_po_id.id or
            self.product_uom.id,
            'product_qty': self.product_uom_qty,
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


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    partner_id = fields.Many2one(
        'res.partner', 'Contact', check_company=False, states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})


class StockMove(models.Model):
    _inherit = "stock.move"

    picking_id = fields.Many2one('stock.picking', 'Transfer', index=True, states={'done': [('readonly', True)]}, check_company=False)
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', check_company=False)
    inventory_id = fields.Many2one('stock.inventory', 'Inventory', check_company=False)
    route_ids = fields.Many2many('stock.location.route', 'stock_location_route_move', 'move_id', 'route_id', 'Destination route', help="Preferred route", check_company=False)


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    picking_id = fields.Many2one(
        'stock.picking', 'Transfer', auto_join=True,
        check_company=False,
        index=True,
        help='The stock operation where the packing has been made')


class Picking(models.Model):
    _inherit = "stock.picking"

    location_id = fields.Many2one(
        'stock.location', "Source Location",
        default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_src_id,
        check_company=False, readonly=True, required=True,
        states={'draft': [('readonly', False)]})
    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location",
        default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_dest_id,
        check_company=False, readonly=True, required=True,
        states={'draft': [('readonly', False)]})