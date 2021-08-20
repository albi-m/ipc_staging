from odoo import api, fields, models,_




class SaleOrderCustom(models.Model):
    _inherit = 'sale.order'

    vendor_id = fields.Char(string="BP Code", compute='_get_vendor_id')
    ref_order_id = fields.Char(string="Reference Order Id")
    total_quantity = fields.Float(string='Total Quantity', compute='_get_total_quantity')

    def _get_total_quantity(self):
        qty = 0
        for rec in self:
            for r in rec.order_line:
                qty += r.product_uom_qty
        self.total_quantity = qty

    def _get_vendor_id(self):
        self.vendor_id = self.partner_id.customer_code


class SaleOrderLineCustom(models.Model):
    _inherit = 'sale.order.line'

    product_code = fields.Char(string='Product code', compute='_get_product_code')

    def _get_product_code(self):
        for rec in self:
            rec.product_code = rec.product_id.default_code

