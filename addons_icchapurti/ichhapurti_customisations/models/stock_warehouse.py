# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockWarehouse(models.Model):
    _name = 'resupply.route.wizard'

    def apply_route(self):
        if self.env.company.parent_id:
            warehouses = self.env['stock.warehouse'].sudo().search([])
            for warehouse in warehouses:
                if warehouse.company_id.parent_id:
                    warehouse.resupply_wh_ids = warehouse.company_id.parent_id.default_wh
                    warehouse.show_resupply = True
            route = self.env['stock.location.route'].sudo().search([('company_id', '=', self.env.company.id),
                                                             ('product_selectable', '=', True)])

            products = self.env['product.template'].sudo().search([]).write({'route_ids': (4, route.id)})

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def apply_buy_mto(self):
        mto = self.env['stock.location.route'].sudo().browse(1)
        buy = self.env['stock.location.route'].sudo().browse(5)
        mto.active = True
        products = self.env['product.template'].sudo().search([]).write(
            {'route_ids': [(4, mto.id), (4, buy.id)]})
        test_vendor = self.env['res.partner'].search([
            ('name', '=', 'Test Vendor')], limit=1)
        if not test_vendor:
            test_vendor = self.env['res.partner'].create({
                'name': "Test Vendor"
            })
        print(test_vendor)
        vals = {
            'name': test_vendor.id,
        }
        products = self.env['product.template'].sudo().search([('seller_ids', '=', False)]).write({
            'seller_ids': [(0, 0, vals)]
        })


class ResCompany(models.Model):
    _inherit = 'res.company'

    default_wh = fields.Many2one('stock.warehouse', string="Default Warehouse")


class WarehouseCheck(models.Model):
    _inherit = 'sale.order'

    def _compute_warehouse_user(self):
        for rec in self:
            rec.warehouse_user = True
            rec.display_record = True
            if not self.env.user.property_warehouse_id:
                rec.display_record = True
            elif self.env.user.property_warehouse_id != rec.warehouse_id:
                rec.display_record = False

    warehouse_user = fields.Boolean(compute=_compute_warehouse_user)
    display_record = fields.Boolean()
    my_activity_date_deadline = fields.Datetime()


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    allowed_user_ids = fields.One2many('res.users', 'property_warehouse_id',
                                   string="Allowed Users")
