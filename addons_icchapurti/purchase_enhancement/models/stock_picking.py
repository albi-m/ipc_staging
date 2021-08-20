from odoo import api, fields, models,_



class StockMoveLineIn(models.Model):
    _inherit = 'stock.move'


    product_barcode = fields.Char(string='Barcode', compute='_get_product_barcode')
    total_qty = fields.Char(string='Total Done Quantity')
    product_mrp = fields.Float(string='MRP', compute='_get_product_mrp')
    move_bool = fields.Boolean(string="Bool", compute='_get_bool_pick')
    # product_unit_price = fields.Char(string='MRP', compute='_get_product_unit_price')
    product_case_size = fields.Char(string='Case Size', compute='_get_product_case_size')
    product_tax = fields.Char(string='Taxes', compute='_get_product_tax')
    product_hsn_code = fields.Char(string='HSN Code', compute='_get_product_hsn_code')


    def _get_bool_pick(self):
        for rec in self:
            if rec.picking_code == 'incoming':
                rec.move_bool = True
            else:
                rec.move_bool = False

    @api.depends('product_id')
    def _get_product_barcode(self):
        for rec in self:
            rec.product_barcode = rec.product_id.barcode

    # @api.depends('product_id')
    # def _get_product_unit_price(self):
    #     for rec in self:
    #         rec.product_unit_price = rec.product_id.barcode

    @api.depends('product_id')
    def _get_product_mrp(self):
        for rec in self:
            rec.product_mrp = rec.product_id.mrp

    @api.depends('product_id')
    def _get_product_case_size(self):
        for rec in self:
            if rec.picking_code == 'incoming':
                rec.product_case_size = rec.product_id.case_size
            else:
                rec.product_case_size = 0


    @api.depends('product_id')
    def _get_product_tax(self):
        for rec in self:
            if rec.picking_code == 'incoming':
                rec.product_tax = rec.product_id.taxes_id.name
            else:
                rec.product_tax = 0

    @api.depends('product_id')
    def _get_product_hsn_code(self):
        for rec in self:
            if rec.picking_code == 'incoming':
                rec.product_hsn_code = rec.product_id.l10n_in_hsn_code
            else:
                rec.product_hsn_code = 0

class StockPickingIn(models.Model):
    _inherit = 'stock.picking'

    total_demand = fields.Float(string='Total Demand Qty', compute='get_total_demand_qty')

    def get_total_demand_qty(self):
        for rec in self:
            qty_total = 0
            for line in rec.move_ids_without_package:
                qty_total += line.product_uom_qty
                self.total_demand = qty_total
