# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class AssignVendor(models.TransientModel):
    _name = 'assign.vendor'

    po_ids = fields.Many2many('purchase.order', string='Purchase Orders')
    select_all = fields.Boolean("Select All PO")

    def assign_vendor(self):
        if self.po_ids:
            po_ids = self.po_ids
            for po in po_ids:
                print("Purchase Order : ", po.name)
                try:
                    po.assign_vendor_checked = True
                except UserError:
                    continue
                for item in po.order_line:
                    if item.product_id.seller_ids:
                        flag = False
                        for vendor in item.product_id.seller_ids:
                            if vendor.name.id == po.partner_id.id:
                                flag = True
                        if not flag:
                            vals = {
                                'name': po.partner_id.id,
                                'price': item.price_unit
                            }
                            item.product_id.write({
                                'seller_ids': [(0, 0, vals)]
                            })
                    else:
                        vals = {
                            'name': po.partner_id.id,
                            'price': item.price_unit
                        }
                        item.product_id.write({
                            'seller_ids': [(0, 0, vals)]
                        })
            return True

        if self.select_all:
            po_count = self.env['purchase.order'].search_count(
                [('assign_vendor_checked', '=', False)])
            offset = 0
            limit = 100
            while limit <= po_count:
                po_ids = self.env['purchase.order'].search(
                    [('assign_vendor_checked', '=', False)], offset=offset, limit=limit)
                for po in po_ids:
                    print("Purchase Order : ", po.name)
                    try:
                        po.assign_vendor_checked = True
                    except UserError:
                        continue
                    for item in po.order_line:
                        if item.product_id.seller_ids:
                            flag = False
                            for vendor in item.product_id.seller_ids:
                                if vendor.name.id == po.partner_id.id:
                                    flag = True
                            if not flag:
                                vals = {
                                    'name': po.partner_id.id,
                                    'price': item.price_unit
                                }
                                item.product_id.write({
                                    'seller_ids': [(0, 0, vals)]
                                })
                        else:
                            vals = {
                                'name': po.partner_id.id,
                                'price': item.price_unit
                            }
                            item.product_id.write({
                                'seller_ids': [(0, 0, vals)]
                            })
                offset = limit
                limit = limit + 100
            return True
