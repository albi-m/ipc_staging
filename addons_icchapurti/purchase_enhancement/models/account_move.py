# -*- coding: utf-8 -*-
from odoo import api, fields, models,_

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    mvl_pack_size = fields.Float(string='Pack Size')
    barcode = fields.Char(related='product_id.barcode', string='Ean13 barcode')
    default_code = fields.Char(related='product_id.default_code',string='Internal Reference')
    taxable_amount = fields.Float(compute="_cal_taxable_amount", string='Taxable amount')
    tax_rate = fields.Integer(compute="get_taxes", string='Tax Amount')
    sgst_tax = fields.Float(compute='get_sgst', string="SGST")
    igst_tax = fields.Float(compute='get_igst', string="IGST")
    invoice_CGST = fields.Float(compute='get_sgst', string="CGST Tax Rate")
    invoice_SGST = fields.Float(compute='get_sgst', string="SGST Tax Rate")
    invoice_IGST = fields.Float(compute='get_igst', string="IGST Tax Rate")




    @api.depends('product_id', 'quantity', 'price_total', 'tax_ids', 'price_subtotal', 'price_unit')
    def _cal_taxable_amount(self):
        for rec in self:
            rec.taxable_amount = rec.quantity * rec.price_unit

    def get_taxes(self):
        for rec in self:
            if rec.tax_ids:
                for i in rec.tax_ids:
                    if i.children_tax_ids:
                        for j in i.children_tax_ids:
                            tax = 0.0
                            taxs = tax+j.amount
                            get_tax = taxs*2
                            rec.tax_rate = get_tax
                    else:
                        rec.tax_rate = i.amount
            else:
                rec.tax_rate = 0.0

    def get_sgst(self):
        for rec in self:
            if rec.tax_ids and rec.move_id.fiscal_position_id.name != 'Inter State':
                for i in rec.tax_ids:
                    if i.children_tax_ids:
                        for j in i.children_tax_ids:
                            tax = 0.0
                            taxs = tax+j.amount
                            get_tax = taxs
                            rec.invoice_CGST = rec.invoice_SGST = taxs
                            rec.sgst_tax = (get_tax/100)*rec.price_subtotal
                    else:
                        rec.invoice_CGST = rec.invoice_SGST = i.amount / 2
                        rec.sgst_tax = ((i.amount / 100) * rec.price_subtotal) / 2
            else:
                rec.sgst_tax = rec.invoice_CGST = rec.invoice_SGST = 0.0

    def get_igst(self):
        for rec in self:
            if rec.tax_ids and rec.move_id.fiscal_position_id.name == 'Inter State':
                for i in rec.tax_ids:
                    if i.children_tax_ids:
                        tax = 0.0
                        for j in i.children_tax_ids:
                            tax += j.amount
                        rec.invoice_IGST = tax
                        rec.igst_tax = (tax / 100) * rec.price_subtotal
                    else:
                        rec.invoice_IGST = i.amount
                        rec.igst_tax = (i.amount/100) * rec.price_subtotal
            else:
                rec.igst_tax = rec.invoice_IGST = 0.0


class AccountMove(models.Model):
    _inherit = 'account.move'

    ref_order_id = fields.Char(string="Reference Order Id")
