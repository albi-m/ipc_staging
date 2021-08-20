# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError, ValidationError
from io import StringIO
import xlrd
import base64
import re
import psycopg2


class ImportInventory(models.TransientModel):
    _name = 'import.inventory'
    _description = 'Import Inventory Adjustment Data'

    # def _get_warehouses(self):
    #     for rec in self:
    #         company_id = rec.env.company
    #         warehouse = self.env['stock.warehouse'].search([('company_id', '=', company_id.id)])
    #         if len(warehouse) == 1:
    #             self.write({'warehouse': warehouse.id})
    #         return {
    #             'domain': {'warehouse': [('company_id', '=', company_id.id)]}}

    inventory_ref = fields.Char("Inventory Reference", required=True)
    file_upload = fields.Binary("XLSX Sheet", required=True)
    auto_validate = fields.Boolean("Auto Validate Product Move")
    warehouse = fields.Many2one('stock.warehouse', default=lambda self: self.env['stock.warehouse'].search([]), required=True)

    def import_data(self):
        if self.file_upload:
            workbook = xlrd.open_workbook(
                file_contents=base64.decodebytes(self.file_upload))
            for sheet in workbook.sheets():
                index = 1
                inventory_lines = []
                not_available_products = []
                for row in range(sheet.nrows):
                    if row >= 1:
                        row_values = sheet.row_values(row)
                        internal_ref = row_values[index]
                        if isinstance(internal_ref, float):
                            internal_ref = str(int(internal_ref))
                        else:
                            internal_ref = str(internal_ref)
                        qty = row_values[3]
                        product_id = self.env['product.product'].search(
                            [('default_code', '=', internal_ref)])
                        if not product_id:
                            not_available_products.append(
                                (internal_ref, row_values[2]))
                        if len(product_id) > 1:
                            product_id = product_id[1]
                        if product_id.type == 'product':
                            location_id = self.warehouse.lot_stock_id
                            product_id.standard_price = row_values[4]
                            line_ids = (0, 0, {
                                'product_id': product_id.id,
                                'product_uom_id': product_id.uom_id.id,
                                'product_qty': qty,
                                'location_id': location_id.id
                            })
                            inventory_lines.append(line_ids)
                stock_inventory = self.env['stock.inventory'].create({
                    'name': self.inventory_ref,
                    'line_ids': inventory_lines
                })
                stock_inventory.action_start()
                if self.auto_validate:
                    stock_inventory.action_validate()
        if not_available_products:
            message = "The following items are not available in the database"
            for items in not_available_products:
                message = message + "\n" + str(items[1]) + " (" + str(
                    items[0]) + ")"

            raise ValidationError(message)
