# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models,fields,api


class AccountMove(models.Model):
    _inherit = "account.move"
    # Split the product based on HSN code

    company_address = fields.Char(string='Cooperate Address', compute='get_detailed_address')
    total_qty = fields.Integer(string='Total Qty', compute='get_total_qty')
    total_tax = fields.Float(string='Total Qty', compute='get_taxes')
    total_taxable_amount = fields.Float(string='Total Tax Amount', compute='get_total_amt_taxable')
    total_sgst = fields.Float(string="Toatl SGST", compute="get_total_sgst")
    total_igst = fields.Float(string="Toatl SGST", compute="get_total_igst")

    def get_taxes(self):
        self.total_tax = self.amount_total - self.total_taxable_amount

    def get_total_sgst(self):
        for rec in self:
            qty_total = 0
            for line in rec.invoice_line_ids:
                qty_total += line.sgst_tax
                self.total_sgst = qty_total

    def get_total_igst(self):
        for rec in self:
            qty_total = 0
            for line in rec.invoice_line_ids:
                qty_total += line.igst_tax
            self.total_igst = qty_total

    def get_total_amt_taxable(self):
        for rec in self:
            qty_total = 0
            for line in rec.invoice_line_ids:
                qty_total += line.price_subtotal
            rec.total_taxable_amount = qty_total

    def get_total_qty(self):
        for rec in self:
            qty_total = 0
            for line in rec.invoice_line_ids:
                qty_total += line.quantity
                tot = int(qty_total)
                self.total_qty = tot

    def get_detailed_address(self):
        self.company_address = str(self.company_id.street) + str(self.company_id.street2) + ',' + \
                               str(self.company_id.city) + ',' + str(self.company_id.state_id.name) + '-' + \
                               str(self.company_id.zip) + ',' + str(self.company_id.country_id.name)

    def get_hsn_code(self, hsn):
        list1 = []
        for invoice_line in self.invoice_line_ids:
            list1.append(invoice_line.product_id.hsn_code)
        hsn_group = list(set(list1))
        return hsn_group

    def get_items(self):
        list1 = []
        for invoice_line in self.invoice_line_ids:
            list1.append(invoice_line.product_id.hsn_code)
        hsn_group = list(set(list1))
        # move_line1 = self.invoice_line_ids.read_group([('move_id','=', self.id),('product_uom_id', '!=', False),('product_id', '!=', False)],[],'product_id')
        # move_line2 = self.invoice_line_ids.read_group(
        #     [('move_id', '=', self.id), ('product_uom_id', '=', False), ('product_id', '!=', False)],
        #     ['product_id', 'price_unit', 'price_total', 'tax_base_amount'], 'product_id')
        # for rec in move_line1:
        #     products = self.env['product.product'].search([('id', '=', rec['product_id'][0])])
        #     move_line3 = self.invoice_line_ids.read_group([('move_id','=',self.id),('product_uom_id', '=', False),],['price_unit'],'product_id')
        #     product_hsn = products.hsn_code
        #
        # return product_hsn

    def get_total_taxable_amount(self):
        total = 0
        for invoice_line in self.invoice_line_ids:
            total = invoice_line.quantity * invoice_line.price_unit

        return total

    # Group the invoice lines based on hsn number
    def get_hsn_grouped(self, inv_obj):
        if inv_obj:
            hsn_ids = []
            hsn_lines_grouped = []
            for line in inv_obj.invoice_line_ids:
                if line.product_id.hsn_code not in hsn_ids:
                    hsn_ids.append(line.product_id.hsn_code)
            for hsn in hsn_ids:
                vals = [x for x in inv_obj.invoice_line_ids if x.product_id.hsn_code == hsn]
                hsn_lines_grouped.append(vals)

            hsn_vals = []
            for l in range(len(hsn_lines_grouped)):
                hsn_code = False
                hsn_subtotal = hsn_taxes = hsn_total = cgst_rate = cgst_amt = sgst_rate = \
                    sgst_amt = igst_rate = igst_amt = 0
                for inv_line in hsn_lines_grouped[l]:
                    hsn_code = inv_line.product_id.hsn_code
                    hsn_subtotal += inv_line.price_subtotal
                    cgst_rate = inv_line.invoice_CGST
                    sgst_rate = inv_line.invoice_SGST
                    igst_rate = inv_line.invoice_IGST
                    cgst_amt += round((cgst_rate / 100) * inv_line.price_subtotal, 2)
                    sgst_amt += round((sgst_rate / 100) * inv_line.price_subtotal, 2)
                    igst_amt += round((igst_rate / 100) * inv_line.price_subtotal, 2)
                hsn_taxes = cgst_amt + sgst_amt + igst_amt
                hsn_total = hsn_subtotal + hsn_taxes
                hsn_vals.append([hsn_code, hsn_subtotal, cgst_rate, cgst_amt, sgst_rate,
                                 sgst_amt, igst_rate, igst_amt, hsn_taxes, hsn_total])
            return hsn_vals

    def get_gst(self, inv_id, product_id):
        invoice = self.search([('id', '=', inv_id)], limit=1)
        tax_amount = 0
        rate = 0
        for num in invoice.invoice_line_ids:
            if num.product_id.id == product_id:
                tax_rate = 0
                for i in num.tax_ids:
                    if i.children_tax_ids:
                        tax_rate = (sum(i.children_tax_ids.mapped('amount')))/2
                tax_amount = ((tax_rate / 100) * num.price_subtotal)
                rate = tax_rate / 2
        return [rate, tax_amount]

    # Get Rate and Amount for IGST product
    def get_igst(self, inv_id, product_id):
        invoice = self.search([('id', '=', inv_id)], limit=1)
        tax_amount = 0
        rate = 0
        for i in invoice.invoice_line_ids:
            if i.product_id.id == product_id:
                tax_rate = 0
                for t in i.tax_ids:
                    if not t.children_tax_ids:
                        tax_rate = t.amount
                tax_amount = (tax_rate / 100) * i.price_subtotal
                rate = tax_rate
        return [rate, tax_amount]

    # Get Rate and Amount for Discount
    def get_disc(self, inv_id, line_id):
        disc_amt = 0
        disc_per = 0
        for i in line_id:
            disc_amt = (i.discount / 100) * i.price_total
            disc_per = i.discount
        return [disc_per, disc_amt]

    # calculate final price
    def get_final_price(self, line):
        final_price = 0
        for i in line:
            final_price = line.price_total
        return final_price


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    # Split the product based on HSN code
    company_address = fields.Char(string='Cooperate Address', compute='get_detailed_address')
    partner_address = fields.Char(string='Vendor Address', compute='get_partner_address')
    total_qty = fields.Integer(string='Total Quantity', compute='get_total_qty')

    def get_partner_address(self):
        if self.partner_id:
            self.partner_address = str(self.partner_id.street) + str(self.partner_id.street2) + ',' + str(self.partner_id.city) + ',' + str(
                self.partner_id.state_id.name) + '-' + str(self.partner_id.zip) + ',' + str(self.partner_id.country_id.name)
        else:
            self.partner_address = ''

    def get_detailed_address(self):
        self.company_address = str(self.company_id.street) + str(self.company_id.street2) +','+str(self.company_id.city) +','+str(self.company_id.state_id.name) +'-'+str(self.company_id.zip) +','+str(self.company_id.country_id.name)

    def get_hsn_code(self, hsn):
        list1 = []
        for pol in self.order_line:
            list1.append(pol.product_id.l10n_in_hsn_code)
        hsn_group = list(set(list1))
        return hsn_group

    # Get Rate and Amount fot GST product
    def get_gst(self, po_id, product_id):
        po = self.search([('id', '=', po_id)], limit=1)
        tax_amount = 0
        rate = 0
        for num in po.order_line:
            if num.product_id.id == product_id:
                tax_rate = 0
                for i in num.taxes_id:
                    if i.children_tax_ids:
                        tax_rate = sum(i.children_tax_ids.mapped('amount'))
                tax_amount = ((tax_rate / 100) * num.price_subtotal) / 2
                rate = tax_rate / 2
        return [rate, tax_amount]

    # Get Rate and Amount fot IGST product
    def get_igst(self, po_id, product_id):
        po = self.search([('id', '=', po_id)], limit=1)
        tax_amount = 0
        rate = 0
        for i in po.order_line:
            if i.product_id.id == product_id:
                tax_rate = 0
                for t in i.taxes_id:
                    if not t.children_tax_ids:
                        tax_rate = t.amount
                tax_amount = (tax_rate / 100) * i.price_subtotal
                rate = tax_rate
        return [rate, tax_amount]

    # Get Rate and Amount for Discount
    def get_disc(self, po_id, line_id):
        disc_amt = 0
        disc_per = 0
        for i in line_id:
            disc_amt = (i.discount / 100) * i.price_total
            disc_per = i.discount
        return [disc_per, disc_amt]

    # calculate final price
    def get_final_price(self, line):
        final_price = 0
        for i in line:
            disc_amt = (i.discount / 100) * i.price_total
            final_price = line.price_total - disc_amt
        return final_price


    def get_total_qty(self):
        qty_total=0
        for rec in self.order_line:
            qty_total += rec.product_qty
        self.total_qty = qty_total

