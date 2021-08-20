# -*- coding: utf-8 -*-

from odoo import models, fields
import xlrd
import base64
from odoo.exceptions import ValidationError


class ImportPO(models.TransientModel):
    _name = "import.purchase.line"
    _description = "Import purchase order lines"

    po_import_file = fields.Binary("PO Sheet")
    product_import_mode = fields.Selection(selection=[
        ('barcode', 'Barcode'), ('default_code', 'Internal Reference')],
        default='default_code')

    def import_pol(self):
        if self.po_import_file:
            workbook = xlrd.open_workbook(
                file_contents=base64.decodebytes(self.po_import_file))
            for sheet in workbook.sheets():
                order_lines = []
                not_available_products = []
                for row in range(sheet.nrows):
                    if row >= 1:
                        row_values = sheet.row_values(row)
                        if row_values[0]:
                            po_sequence = row_values[0]
                        active_po = self.env.context.get('active_ids', [])
                        current_po = self.env['purchase.order'].browse(active_po)
                        if po_sequence != current_po.name:
                            message = "Order numbers doesn't match ! " \
                                      "( The uploaded file is for the Purchase Order " + po_sequence + ")"
                            raise ValidationError(message)
                        if po_sequence:
                            purchase_order = self.env['purchase.order'].search([
                                ('name', '=', po_sequence)])

                        if self.product_import_mode == 'default_code':
                            if row_values[1]:
                                ref = row_values[1]
                                if isinstance(ref, float):
                                    ref = str(int(ref))
                                product_id = self.env['product.product'].search(
                                    [('default_code', '=', ref)]) or self.env['product.product'].search(
                                    [('default_code', 'ilike', ref)], limit=1)
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
                            if product_id.uom_po_id.category_id.id != uom_id.category_id.id:
                                message = "For the product \"" + product_id.name + " [" + product_id.default_code + "] \"" + \
                                          " UoM categories don't match, please replace in the file with a UoM having category \"" + \
                                          product_id.uom_po_id.category_id.name + "\""
                                raise ValidationError(message)
                            case_size = product_id.product_tmpl_id.case_size
                            order_line = (0, 0, {
                                    'name': product_id.name,
                                    'product_id': product_id.id,
                                    'product_qty': row_values[2],
                                    'product_uom': uom_id.id,
                                    'price_unit': row_values[4],
                                    'taxes_id': product_id.taxes_id,
                                    'case_size': case_size
                                })
                            order_lines.append(order_line)
                if not_available_products:
                    message = "The following items are not available in " \
                              "the database. Check if you select the right option" \
                              "(Barcode or Internal Reference)"
                    for items in not_available_products:
                        message = message + "\n" + str(items)
                    raise ValidationError(message)
                if order_lines:
                    purchase_order.write({'order_line': order_lines})
                else:
                    raise ValidationError("No lines to import !")
