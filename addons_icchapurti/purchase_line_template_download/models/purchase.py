# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError
import xlrd, xlsxwriter
import base64

class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'


    purchase_order_line_template = fields.Binary('Purchase Order Line Template')
    filename = fields.Char('FILE NAME', size=250, readonly=True)
    
    def get_purchase_order_line_template(self):
        wb = xlsxwriter.Workbook('purchase_order_line.xls')
        ws = wb.add_worksheet()
        ws.set_landscape()
        ws.fit_to_pages(1, 1)
        
        ws.write('A1', 'Purchase Order No.')
        ws.write('B1', 'Product')
        ws.write('C1', 'Qty')
        ws.write('D1', 'uom')
        ws.write('E1', 'Product Description')
        ws.write('F1', 'Unit Price')
        ws.write('G1', 'Taxes')
        #ws.write('H1', 'Pack Size')

        s = 'purchase_order_line'+'.xls'
        wb.close()
        f = open("purchase_order_line.xls",'rb+')
        out = base64.encodestring(f.read())
        self.write({'purchase_order_line_template': out, 'filename': s})
        f.close()
        return True
