# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError
import xlrd, xlsxwriter
import base64

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'


    sale_order_line_template = fields.Binary('Sale Order Line Template')
    filename = fields.Char('FILE NAME', size=250, readonly=True)
    
    def get_sale_order_line_template(self):
        wb = xlsxwriter.Workbook('sale_order_line.xls')
        ws = wb.add_worksheet()
        ws.set_landscape()
        ws.fit_to_pages(1, 1)
        
        ws.write('A1', 'Sale Order No.')
        ws.write('B1', 'Product')
        ws.write('C1', 'Qty')
        ws.write('D1', 'uom')
        ws.write('E1', 'Product Description')
        ws.write('F1', 'Unit Price')
        #ws.write('F1', 'Taxes')
        ws.write('G1', 'Discount')

        s = 'sale_order_line'+'.xls'
        wb.close()
        f = open("sale_order_line.xls",'rb+')
        out = base64.encodestring(f.read())
        self.write({'sale_order_line_template': out, 'filename': s})
        f.close()
        return True
