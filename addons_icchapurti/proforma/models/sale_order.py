from odoo import models,fields,api,_
from odoo.exceptions import ValidationError



class SaleOrderIn(models.Model):
    _inherit = 'sale.order'

    company_address = fields.Char(string='Cooperate Address', compute='get_detailed_address')
    quantity_total = fields.Integer(string='Total Quantity', compute='get_total_quantity_available')
    tot_sgst = fields.Float(string='Total SGST', compute='get_total_sgst')
    tot_cgst = fields.Float(string='Total CGST', compute='get_total_cgst')
    tot_igst = fields.Float(string='Total IGST', compute='get_total_igst')
    total_tax_amt = fields.Float(string='Total TAX', compute='get_total_tax')
    total_price_subtotal = fields.Float(string='Total Sub Total', compute='get_total_price_subtotal')
    total_amt = fields.Float(string='Total Amount', compute='get_total_amt')

    def get_detailed_address(self):
        self.company_address = str(self.company_id.street) + str(self.company_id.street2) +','+str(self.company_id.city) +','+str(self.company_id.state_id.name) +'-'+str(self.company_id.zip) +','+str(self.company_id.country_id.name)

    def print_proforma(self):
        return self.env.ref('proforma.action_proforma_report').report_action(self)


    def get_total_quantity_available(self):
        for rec in self:
            qty_total = 0
            for line in rec.order_line:
                if line.qty_bool == True:
                    qty_total += line.product_uom_qty
        self.quantity_total = qty_total


    def get_total_sgst(self):
        for rec in self:
            qty_total = 0
            for line in rec.order_line:
                if line.qty_bool == True:
                    qty_total += line.sale_amount_SGST
                    self.tot_sgst = qty_total

    def get_total_cgst(self):
        for rec in self:
            qty_total = 0
            for line in rec.order_line:
                if line.qty_bool == True:
                    qty_total += line.sale_amount_CGST
                    self.tot_cgst = qty_total

    def get_total_igst(self):
        for rec in self:
            qty_total = 0
            for line in rec.order_line:
                if line.qty_bool == True:
                    qty_total += line.sale_amount_IGST
                    self.tot_igst = qty_total

    def get_total_tax(self):
        self.total_tax_amt = self.tot_cgst + self.tot_igst + self.tot_sgst

    def get_total_price_subtotal(self):
        for rec in self:
            qty_total = 0
            for line in rec.order_line:
                if line.qty_bool == True:
                    qty_total += line.price_subtotal
        self.total_price_subtotal = qty_total

    def get_total_amt(self):
        self.total_amt = self.total_tax_amt + self.total_price_subtotal


class SaleOrderLineIn(models.Model):
    _inherit = 'sale.order.line'



    qty_bool = fields.Boolean(string='QTY AVAIL BOOL', compute='get_qty_available')


    def get_qty_available(self):
        for rec in self:
            if rec.product_uom_qty <= rec.product_id.qty_available:
                rec.qty_bool = True
            elif rec.product_uom_qty > rec.product_id.qty_available:
                rec.qty_bool = False
            else:
                rec.qty_bool = False