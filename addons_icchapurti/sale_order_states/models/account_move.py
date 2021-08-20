# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super(AccountMove, self).action_post()
        sale_order = self.env['sale.order'].sudo().search([('name', '=', self.invoice_origin)])
        print("Please   ", sale_order.check_picking_status())
        if sale_order.check_picking_status():
            print("True aanu")
            sale_order.check_invoice_status()
        else:
            print("True alla")
            sale_order.custom_state = 'invoice_partial'
        return res