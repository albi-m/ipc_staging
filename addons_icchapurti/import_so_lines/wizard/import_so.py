# -*- coding: utf-8 -*-

from odoo import models, fields
import xlrd
import base64
from odoo.exceptions import ValidationError


class ImportSOLines(models.TransientModel):
    _name = "import.sales.line"
    _description = "Import sale order lines"

    so_import_file = fields.Binary("SO Sheet")
    product_import_mode = fields.Selection(selection=[
        ('barcode', 'Barcode'), ('default_code', 'Internal Reference')],
        default='default_code')

    def import_sol(self):
        if self.so_import_file:
            workbook = xlrd.open_workbook(
                file_contents=base64.decodebytes(self.so_import_file))
            for sheet in workbook.sheets():
                order_lines = []
                not_available_products = []
                for row in range(sheet.nrows):
                    if row >= 1:
                        row_values = sheet.row_values(row)
                        if row_values[0]:
                            so_sequence = row_values[0]
                        active_so = self.env.context.get('active_ids', [])
                        current_so = self.env['sale.order'].browse(active_so)
                        if so_sequence != current_so.name:
                            message = "Order numbers doesn't match ! " \
                                      "( The uploaded file is for the Sale Order " + so_sequence + ")"
                            raise ValidationError(message)
                        if so_sequence:
                            sale_order = self.env['sale.order'].search([
                                ('name', '=', so_sequence)])

                        if self.product_import_mode == 'default_code':
                            if row_values[1]:
                                ref = row_values[1]
                                if isinstance(ref, float):
                                    ref = str(int(ref))
                                product_id = self.env['product.product'].search(
                                    [('default_code', '=', ref)])
                                if not product_id:
                                    not_available_products.append(ref)
                                if len(product_id) > 1:
                                    raise ValidationError(
                                        "There are two or more products "
                                        "with same Internal Reference\nDuplicate Internal Reference : " + ref)
                            else:
                                product_id = False
                        else:
                            if row_values[1]:
                                barcode = row_values[1]
                                if isinstance(barcode, float):
                                    barcode = str(int(barcode))
                                product_id = self.env['product.product'].search(
                                    [('barcode', '=', barcode)])
                                if not product_id:
                                    not_available_products.append(barcode)
                                if len(product_id) > 1:
                                    raise ValidationError(
                                        "There are two or more products "
                                        "with same Barcode\nDuplicate Barcode : " + barcode)
                            else:
                                product_id = False
                        if row_values[3]:
                            uom_id = self.env['uom.uom'].search(
                                [('name', 'like', row_values[3])], limit=1)
                            if not uom_id:
                                raise ValidationError("The given uom doesn't exist (" + row_values[3] + ")")
                        if product_id:
                            order_line = (0, 0, {
                                    'name': product_id.name,
                                    'product_id': product_id.id,
                                    'product_uom_qty': row_values[2],
                                    'product_uom': uom_id.id,
                                    'price_unit': row_values[4],
                                    'discount': row_values[5]
                                })
                            order_lines.append(order_line)
                if not_available_products:
                    message = "The following items are not available in " \
                              "the database. Check if you select the right option" \
                              "(Barcode or Internal Reference)"
                    for items in not_available_products:
                        message = message + "\n" + str(items)
                    raise ValidationError(message)
                print(order_lines)
                if order_lines:
                    sale_order.write({'order_line': order_lines})
                else:
                    raise ValidationError("No lines to import !")
