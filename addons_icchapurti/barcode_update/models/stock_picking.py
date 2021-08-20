from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



class StockPickIn(models.Model):
    _inherit = 'stock.picking'


    input_barcode = fields.Char('Input Barcode')
    vendor_address = fields.Char('Vendor Address', compute='get_vendor_address')
    boool = fields.Boolean('Bool', compute='get_bool')

    def click_simulate(self):
        return True

    def get_bool(self):
        if self.picking_type_id.code == 'incoming':
            self.boool = True
        else:
            self.boool = False

    def get_vendor_address(self):
        order = self.env['purchase.order'].search([('name', '=', self.origin)])
        if self.picking_type_id.id == 1:
            self.vendor_address = order.partner_address
        else:
            self.vendor_address = False

    @api.onchange('input_barcode')
    def update_quantities(self):
        if self.picking_type_id.code == 'incoming':
            barcode_check = 0
            for rec in self.move_ids_without_package:
                if rec.product_id.barcode and rec.product_id.barcode == self.input_barcode:
                    barcode_check += 1
                else:
                    barcode_check = barcode_check
            if barcode_check == 1:
                for rec in self.move_ids_without_package:
                    # print("rec outgoing", rec)
                    if rec.quantity_done <= rec.product_uom_qty:
                        if rec.product_id.barcode and rec.product_id.barcode == self.input_barcode:
                            rec.quantity_done = 1 + rec.quantity_done
                            rec.sort_field = 1
                            self.input_barcode = ''
                            if rec.product_uom_qty < rec.quantity_done:
                                raise ValidationError("Demand is Reached")
                        else:
                            rec.sort_field = 0
                    else:
                        raise ValidationError("Done Quantities Cannot be more than Demand Quantities")
            else:
                raise ValidationError("Barcode Doesnot match with the products present")

    @api.onchange('input_barcode')
    def update_dc_quantities(self):
        if self.picking_type_id.code == 'outgoing':
            barcode_check = 0
            for rec in self.move_ids_without_package:
                if rec.product_id.barcode and rec.product_id.barcode == self.input_barcode:
                    barcode_check += 1
                else:
                    barcode_check = barcode_check
            if barcode_check == 1:
                for rec in self.move_ids_without_package:
                    if rec.quantity_done <= rec.product_uom_qty:
                        if rec.product_id.barcode and rec.product_id.barcode == self.input_barcode:
                            rec.quantity_done = 1 + rec.quantity_done
                            rec.sort_field = 1
                            self.input_barcode = ''
                            if rec.product_uom_qty < rec.quantity_done:
                                raise ValidationError("Demand is Reached")
                        else:
                            rec.sort_field = 0
                    else:
                        raise ValidationError("Done Quantities Cannot be more than Demand Quantities")
            else:
                raise ValidationError("Barcode Doesnot match with the products present")


class StockMove(models.Model):
    _inherit = 'stock.move'

    sort_field = fields.Integer()

    @api.constrains('quantity_done')
    def validation_on_done(self):
        for rec in self:
            if rec.quantity_done > rec.product_uom_qty:
                raise ValidationError("Done Quantities Cannot Be More Than Demand Quantities")
