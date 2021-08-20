# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    warehouse_role = fields.Selection([('user', 'User'), ('admin', 'Admin')],
                                    string="Warehouse role", default='admin')
    allowed_warehouse_ids = fields.Many2many('stock.warehouse',
                                             string="Allowed Warehouses")
    allowed_location_ids = fields.Many2many('stock.location',
                                            string="Allowed Locations")
    set_all_admin = fields.Boolean(default=False)

    @api.onchange('warehouse_role')
    def apply_warehouse(self):
        if self.warehouse_role == 'admin':
            self.allowed_warehouse_ids = self.env['stock.warehouse'].search([])
            location_ids = []
            for rec in self.allowed_warehouse_ids:
                location_ids.append(rec.lot_stock_id.id)
            self.allowed_location_ids = location_ids
            if not self.set_all_admin:
                users = self.env['res.users'].search(
                    [('warehouse_role', '=', 'admin')])
                users.allowed_warehouse_ids = self.env['stock.warehouse'].search([])
                users.allowed_location_ids = location_ids
                users.set_all_admin = True
        else:
            self.allowed_warehouse_ids = False
            self.allowed_location_ids = False

    @api.onchange('allowed_warehouse_ids')
    def get_location(self):
        if self.warehouse_role == 'user':
            location_ids = []
            for rec in self.allowed_warehouse_ids:
                location_ids.append(rec.lot_stock_id.id)
            self.allowed_location_ids = location_ids
