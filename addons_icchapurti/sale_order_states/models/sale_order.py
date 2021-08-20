# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOderStatus(models.Model):
    _inherit = 'sale.order'

    def _check_status(self):
        self.check_status = True
        if self.picking_ids:
            self.check_picking_status()
        if self.invoice_ids:
            self.check_invoice_status()

    custom_state = fields.Selection(string="Order Status", selection=[
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('sale', 'Sale Order'),
        ('picking_created', 'Picking Created'),
        ('picking_partial', 'Picking Partially Validated'),
        ('picking_validate', 'Picking Validated'),
        ('invoice_draft', 'Invoice Created'),
        ('invoice_partial', 'Partially Invoice Posted'),
        ('invoice_posted', 'Invoice Posted'),
        ('done', 'Locked')
    ], default='done')
    sale_invoice_ids = fields.Many2many('account.move')
    check_status = fields.Boolean(compute=_check_status)

    @api.model
    def create(self, vals):
        res = super(SaleOderStatus, self).create(vals)
        res['custom_state'] = 'draft'
        return res

    def action_unlock(self):
        res = super(SaleOderStatus, self).action_unlock()
        if self.picking_ids:
            print(self.check_picking_status())
        if self.invoice_ids:
            self.check_invoice_status()
        return res

    def check_invoice_status(self):
        flag = 1
        count = 0
        if self.invoice_ids:
            for rec in self.invoice_ids:
                if rec.state == 'posted':
                    count += 1
                if rec.state not in ['posted', 'cancel']:
                    self.custom_state = 'invoice_draft'
                    if count > 0:
                        self.custom_state = 'invoice_partial'
                    return 'invoice_partial'
            picking_status = self.check_picking_status()

            if picking_status != 'picking_validate':
                self.custom_state = 'invoice_partial'
                return 'invoice_partial'
            if count and count == len(self.invoice_ids):
                self.custom_state = 'invoice_posted'
                return 'invoice_posted'
            else:
                self.custom_state = 'invoice_partial'
                return 'invoice_partial'

    def check_picking_status(self):
        count = 0
        if self.picking_ids:
            for rec in self.picking_ids:
                if rec.state == 'done':
                    count += 1
                if rec.state not in ['done', 'cancel']:
                    self.custom_state = 'picking_created'
                    return 'picking_created'
        if count and count == len(self.picking_ids):
            self.custom_state = 'picking_validate'
            return 'picking_validate'
        else:
            self.custom_state = 'picking_partial'
            return 'picking_partial'

    def _create_invoices(self, final=False):
        res = super(SaleOderStatus, self)._create_invoices()
        self.write({
            'sale_invoice_ids': [(4, res.id)]
        })
        self.custom_state = 'invoice_draft'
        return res

    def _action_confirm(self):
        res = super(SaleOderStatus, self)._action_confirm()
        print("Haha----------------")
        for rec in self:
            rec.custom_state = 'picking_created'
        return res
