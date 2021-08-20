# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def update_qty_delivered(self):
        for rec in self:
            done_qty = []
            first_loop = True
            exist = False
            for picking in rec.picking_ids:
                if picking.state == 'done':
                    for line in picking.move_ids_without_package:
                        print(line.product_id.id)
                        if first_loop:
                            done_qty.append(
                                [line.product_id.id, line.quantity_done])
                            first_loop = False
                            continue
                        for item in done_qty:
                            if line.product_id.id == item[0]:
                                item[1] = item[1] + line.quantity_done
                                exist = True
                        if not exist:
                            done_qty.append([line.product_id.id, line.quantity_done])
                            exist = False

            for order in self.order_line:
                for item in done_qty:
                    if order.product_id.id == item[0]:
                        order.qty_delivered = item[1]

    def update_tax(self):
        for line in self.order_line:
            product = line.product_id.id
            lst_price = line.product_id.lst_price
            unit_price = lst_price
            quantity = line.product_uom_qty
            price_tax = 0.0
            price_subtotal = 0.0
            price_total = 0.0
            group_tax = 0.0

            for tax in self.order_line.tax_id:
                if tax.amount_type == "percent":
                    tax_percent = tax.amount
                    unit_price = round(lst_price / (1 + (tax_percent/100) ), 2)
                    price_tax = round((tax_percent * unit_price * quantity/100), 2)
                    price_subtotal = round((unit_price * quantity),2)
                if tax.amount_type == "group":
                    for child_tax_amount in tax.children_tax_ids:
                        group_tax += child_tax_amount.amount
                    tax_percent = group_tax
                    unit_price = round(lst_price / (1 + (tax_percent/100) ), 2)
                    price_tax = round((tax_percent * unit_price * quantity/100), 2)
                    price_subtotal = round((unit_price * quantity),2)

            line.price_unit = unit_price
            line.price_tax = price_tax
            line.price_subtotal = price_subtotal
            line.price_total = round((price_tax + price_subtotal), 2)
            line.product_mrp = line.product_id.mrp
            

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id')
    def _compute_mrp(self):
        for order in self:
            for line in order:
                line.product_mrp = line.product_id.mrp
                line.case_size = line.product_id.case_size

    product_mrp = fields.Float(string="MRP", compute='_compute_mrp', store=True)
    case_size = fields.Float(string="Case Size", compute='_compute_mrp', store=True)