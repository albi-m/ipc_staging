# -*- coding: utf-8 -*-

from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    add_purchase_vendor = fields.Boolean(string="Assign Purchase Vendor",
                                         default=True)
    assign_vendor_checked = fields.Boolean(default=False)

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        if self.add_purchase_vendor:
            self.assign_vendor_checked = True
            for item in self.order_line:
                if item.product_id.seller_ids:
                    flag = False
                    for vendor in item.product_id.seller_ids:
                        if vendor.name.id == self.partner_id.id:
                            flag = True
                    if not flag:
                        vals = {
                            'name': self.partner_id.id,
                            'price': item.price_unit
                        }
                        item.product_id.write({
                            'seller_ids': [(0, 0, vals)]
                        })
                else:
                    vals = {
                        'name': self.partner_id.id,
                        'price': item.price_unit
                    }
                    item.product_id.write({
                        'seller_ids': [(0, 0, vals)]
                    })
        return res
