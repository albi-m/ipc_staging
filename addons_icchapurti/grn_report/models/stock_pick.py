from odoo import models,fields,api,_
from odoo.exceptions import ValidationError



class StockPickIn(models.Model):
    _inherit = 'stock.picking'

    company_address = fields.Char(string='Cooperate Address', compute='get_detailed_address')
    warehouse_address = fields.Char(string='WareHouse Address', compute='get_warehouse_address')
    vendor_invoice = fields.Char(string='Vendor Invoice Number')
    total_qty = fields.Char(string='Total Done Quantity', compute='get_total_qty')
    total_amount = fields.Char(string='Total Amt', compute='get_total_amt')
    current_user = fields.Char('Current User', default=lambda self: self.env.uid)


    def get_total_amt(self):
        for rec in self:
            amt_total = 0
            for line in rec.move_ids_without_package:
                amt_total += line.total_price
                self.total_amount = amt_total



    def get_total_qty(self):
        for rec in self:
            qty_total = 0
            for line in rec.move_ids_without_package:
                qty_total += line.quantity_done
                self.total_qty = qty_total


    def get_detailed_address(self):
        self.company_address = str(self.company_id.street) + str(self.company_id.street2) +','+str(self.company_id.city) +','+str(self.company_id.state_id.name) +'-'+str(self.company_id.zip) +','+str(self.company_id.country_id.name)


    def get_warehouse_address(self):
        obj = self.picking_type_id.warehouse_id.partner_id
        self.warehouse_address = str(obj.street) + str(obj.street2) +','+str(obj.city) +','+str(obj.name) +'-'+str(obj.zip) +','+str(obj.name)




















class StockMoveInherit(models.Model):
    _inherit ='stock.move'



    total_price = fields.Integer(string="Total", compute="get_total")



    def get_total(self):
        for rec in self:
            rec.total_price = rec.price_unit * rec.quantity_done
