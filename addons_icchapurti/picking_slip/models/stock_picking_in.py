from odoo import api, fields, models,_




class StockPickingIn(models.Model):
    _inherit = 'stock.picking'

    total_reserved = fields.Float(string='Total Demand Qty', compute='_get_total_remand_qty')
    shipping_date = fields.Char(string='Shipping Date', compute='_get_shipping_date')
    invoice_num = fields.Char(string='Invoice Number', compute='_get_invoice_number')
    ref_id = fields.Char(string='Reference Id', compute='_get_reference_id')
    total_mrp = fields.Float(string="Total MRP", compute='_get_total_mrp')
    total_sale_price = fields.Float(string="Total Sale Price", compute='_get_total_sp')


    def _get_total_mrp(self):
        for rec in self:
            total = 0.0
            for line in rec.move_ids_without_package:
                if line.forecast_availability > 1:
                    total += line.product_mrp
            rec.total_mrp = total

    def _get_total_sp(self):
        for rec in self:
            total = 0.0
            for line in rec.move_ids_without_package:
                if line.forecast_availability > 1:
                    total += line.product_sale_price
            rec.total_sale_price = total


    def _get_total_remand_qty(self):
        for rec in self:
            qty_total = 0
            for line in rec.move_ids_without_package:
                qty_total += line.forecast_availability
                self.total_reserved = qty_total


    def _get_shipping_date(self):
        self.shipping_date = self.scheduled_date.date()


    def _get_reference_id(self):
        sale_order = self.env['sale.order'].search([('name', '=', self.origin)])
        self.ref_id = sale_order.ref_order_id


    def _get_invoice_number(self):
        invoice = self.env['account.move'].search([('invoice_origin', '=', self.origin)])
        if invoice.move_type == 'out_invoice':
            self.invoice_num = invoice.name
        else:
            self.invoice_num = 'Invoice not Created or Validated'


    @api.onchange('vendor_invoice')
    def get_pack_grouped(self):
        pack_ids = []
        package_grouped = []
        for line in self.move_line_ids_without_package:
            if line.result_package_id not in pack_ids:
                pack_ids.append(line.result_package_id)
        for packs in pack_ids:
            vals = [x for x in self.move_line_ids_without_package if x.result_package_id == packs]
            package_grouped.append(vals)

        pack_vals = []
        for l in range(len(package_grouped)):
            pack_no = False
            quantity = 0
            total = 0
            for line in package_grouped[l]:
                pack_no = line.result_package_id.name
                quantity = line.result_package_id.total_qty
            pack_vals.append([pack_no,quantity])
        return pack_vals






class StockQtyPack(models.Model):
    _inherit = 'stock.quant.package'



    total_qty = fields.Integer(string='Total Qty', compute='_get_total_qty')


    def _get_total_qty(self):
        for rec in self:
            qty_total = 0
            for line in rec.quant_ids:
                qty_total += line.quantity
            rec.total_qty = qty_total


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_sale_price = fields.Float(string='Sale Price', compute='_get_product_sale_price')



    def _get_product_sale_price(self):
        for rec in self:
            if rec.picking_code == 'outgoing':
                if rec.sale_line_id.product_id == rec.product_id:
                    rec.product_sale_price = rec.sale_line_id.price_unit
                else:
                    rec.product_sale_price = 0
            else:
                rec.product_sale_price = 0
