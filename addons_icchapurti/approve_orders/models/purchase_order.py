# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseApproval(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[
        ('sent', 'RFQ Sent'),
        ('to_confirm', 'Waiting for confirmation'),
        ('to_approve', 'Waiting for Approval'),
        ('purchase', 'Purchase Order')])

    def submit_po(self):
        for rec in self:
            rec.state = 'to_confirm'

    def confirm_po(self):
        for rec in self:
            rec.state = 'to_approve'

    def button_confirm(self):
        res = super(PurchaseApproval, self).button_confirm()
        for order in self:
            print(order.state)
            if order.state not in ['draft', 'sent', 'to_approve']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return res