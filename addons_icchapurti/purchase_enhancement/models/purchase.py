# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError

READONLY_STATES = {
    'purchase': [('readonly', True)],
    'done': [('readonly', True)],
    'cancel': [('readonly', True)],
}

class PurchaseLine(models.Model):
    _inherit = 'purchase.order.line'

    pack_size = fields.Float(string='Pack Size')
    replaced = fields.Boolean(string='Replaced')
    product_code = fields.Char(string='Product code', compute='_get_product_code')
    discount = fields.Float(string='Discount')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['company_id'] = self.env.company.id
        res_ids = super(PurchaseLine, self).create(vals_list)
        return res_ids

    def _get_product_code(self):
        for rec in self:
            rec.product_code = rec.product_id.default_code

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    replaced_bool = fields.Boolean(string='All Value', compute='get_bool_value', store=True)
    company_id = fields.Many2one('res.company', 'Company', index=True, states=READONLY_STATES, default=lambda self: self.env.company.id)
    vendor_id = fields.Char(string="Vendor ID", compute='_get_vendor_id')
    total_qty = fields.Float(string="Total Qty")



    # @api.depends('product_qty')
    # def _get_total_quantity(self):
    #     qty = 0
    #     for rec in self.order_line:
    #         qty += rec.product_qty
    #         self.total_qty = qty


    @api.depends('order_line')
    def get_bool_value(self):
        lst = []
        for line in self.order_line:
            lst.append(line.replaced)
            get = any(lst)
            self.replaced_bool = get

    def write(self, vals):
        if self.replaced_bool == True:
            raise UserError(_('Cannot Edit Purchase Order because PO Line was Replaced.'))
        else:
            return super(PurchaseOrder, self).write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['company_id'] = self.env.company.id
        res_ids = super(PurchaseOrder, self).create(vals_list)
        return res_ids

    def _get_vendor_id(self):
        self.vendor_id = self.partner_id.customer_code


class StockPickInherit(models.Model):
    _inherit = 'stock.picking'

    admin_bool = fields.Boolean(string='Is Admin', compute='_get_user_admin')

    def _get_user_admin(self):
        if self.env.user.id == 2:
            self.admin_bool = True
        else:
            self.admin_bool = False

    def get_updated_done_qty(self):
        for rec in self.move_ids_without_package:
            rec.quantity_done  = rec.product_uom_qty

