from odoo import api,models,fields
from xmlrpc import client as xmlrpclib
import xlrd
import base64
from datetime import datetime,timedelta

class StockImport(models.TransientModel):
    _name = 'customer.export'
    _description = 'Data Export'

    file = fields.Binary('File')
    file_name = fields.Char('Document Name')

    def create_stock_jpdpt(self):
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        data = [sheet.row_values(rowx) for rowx in range(1, sheet.nrows)]
        line = []
        product_list = []
        for r in data:
            if r[0]:
                product_rec = self.env['product.product'].search([('available_in_pos', '=', True), ('default_code', '=', r[2])])
                product_list.append(product_rec.id)
                line.append((0, 0, {
                    'product_id': product_rec.id,
                    'product_qty': r[1] if r[1] else 0.0,
                    'location_id': self.env['stock.warehouse'].search([('name', '=', 'JP Departmental Store')], limit=1).lot_stock_id.id,
                }))
        loc = self.env['stock.warehouse'].search([('name', '=', 'JP Departmental Store')], limit=1).lot_stock_id
        stock_inventory_rec = self.env['stock.inventory'].sudo().create({
            'product_ids': [(6, 0, product_list)],
            'location_ids': [(6, 0, loc.ids)],
            #'accounting_date': datetime.now().date() - timedelta(days=38),
            'name': 'JP Departmental Store',
            'line_ids': line
        })
        stock_inventory_rec.action_start()
        stock_inventory_rec.action_validate()

    def create_stock_ggjwh(self):
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        data = [sheet.row_values(rowx) for rowx in range(1, sheet.nrows)]
        line = []
        product_list = []
        for r in data:
            print("rrrrrrrrrrrrrrr", r[2])
            if r[0]:
                r[2] = str(r[2]).replace('.0', '')
                print("tttttttttttttt", r[2])
                product_rec = self.env['product.product'].search([('type', '=', 'product'), ('default_code', '=', r[2])])
                if product_rec:
                    print("eeeeeeeeee", product_rec)
                    product_list.append(product_rec.id)
                    line.append((0, 0, {
                        'product_id': product_rec.id,
                        'product_qty': r[1] if r[1] else 0.0,
                        'location_id': self.env['stock.warehouse'].search([('name', '=', 'GGJ Solutions Pvt. Ltd.')], limit=1).lot_stock_id.id,
                    }))
                    print("OOOOOOOOOOOOOO", product_list)
                    print("pppppppppppppppp", line)
        loc = self.env['stock.warehouse'].search([('name', '=', 'GGJ Solutions Pvt. Ltd.')], limit=1).lot_stock_id
        stock_inventory_rec = self.env['stock.inventory'].sudo().create({
            'product_ids': [(6, 0, product_list)],
            'location_ids': [(6, 0, loc.ids)],
            #'accounting_date': datetime.now().date() - timedelta(days=38),
            'name': 'GGJ STOCK',
            'line_ids': line
        })
        stock_inventory_rec.action_start()
        stock_inventory_rec.action_validate()

    def create_stock_tjngr(self):
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        data = [sheet.row_values(rowx) for rowx in range(1, sheet.nrows)]
        line = []
        product_list = []
        for r in data:
            print("rrrrrrrrrrrrrrr", r[2])
            if r[0]:
                r[2] = str(r[2]).replace('.0', '')
                print("tttttttttttttt", r[2])
                product_rec = self.env['product.product'].search([('type', '=', 'product'), ('default_code', '=', r[2])])
                if product_rec:
                    print("eeeeeeeeee", product_rec)
                    product_list.append(product_rec.id)
                    line.append((0, 0, {
                        'product_id': product_rec.id,
                        'product_qty': r[1] if r[1] else 0.0,
                        'location_id': self.env['stock.warehouse'].search([('name', '=', 'Taj Nagar Warehouse')], limit=1).lot_stock_id.id,
                    }))
                    print("OOOOOOOOOOOOOO", product_list)
                    print("pppppppppppppppp", line)
        loc = self.env['stock.warehouse'].search([('name', '=', 'Taj Nagar Warehouse')], limit=1).lot_stock_id
        stock_inventory_rec = self.env['stock.inventory'].sudo().create({
            'product_ids': [(6, 0, product_list)],
            'location_ids': [(6, 0, loc.ids)],
            #'accounting_date': datetime.now().date() - timedelta(days=38),
            'name': 'TJNGR Stock',
            'line_ids': line
        })
        stock_inventory_rec.action_start()
        stock_inventory_rec.action_validate()

    def create_stock_sbr01_bhagalpur(self):
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        data = [sheet.row_values(rowx) for rowx in range(1, sheet.nrows)]
        line = []
        product_list = []
        for r in data:
            print("rrrrrrrrrrrrrrr", r[2])
            if r[0]:
                r[2] = str(r[2]).replace('.0', '')
                print("tttttttttttttt", r[2])
                product_rec = self.env['product.product'].search([('type', '=', 'product'), ('default_code', '=', r[2])])
                if product_rec:
                    print("eeeeeeeeee", product_rec)
                    product_list.append(product_rec.id)
                    line.append((0, 0, {
                        'product_id': product_rec.id,
                        'product_qty': r[1] if r[1] else 0.0,
                        'location_id': self.env['stock.warehouse'].search([('name', '=', 'SF Bhagalpur')], limit=1).lot_stock_id.id,
                    }))
                    print("OOOOOOOOOOOOOO", product_list)
                    print("pppppppppppppppp", line)
        loc = self.env['stock.warehouse'].search([('name', '=', 'SF Bhagalpur')], limit=1).lot_stock_id
        stock_inventory_rec = self.env['stock.inventory'].sudo().create({
            'product_ids': [(6, 0, product_list)],
            'location_ids': [(6, 0, loc.ids)],
            #'accounting_date': datetime.now().date() - timedelta(days=38),
            'name': 'SBR01 Stock',
            'line_ids': line
        })
        stock_inventory_rec.action_start()
        stock_inventory_rec.action_validate()

    def create_stock_home_guru(self):
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        data = [sheet.row_values(rowx) for rowx in range(1, sheet.nrows)]
        line = []
        product_list = []
        for r in data:
            print("rrrrrrrrrrrrrrr", r[2])
            if r[0]:
                r[2] = str(r[2]).replace('.0', '')
                print("tttttttttttttt", r[2])
                product_rec = self.env['product.product'].search([('type', '=', 'product'), ('default_code', '=', r[2])])
                if product_rec:
                    print("eeeeeeeeee", product_rec)
                    product_list.append(product_rec.id)
                    line.append((0, 0, {
                        'product_id': product_rec.id,
                        'product_qty': r[1] if r[1] else 0.0,
                        'location_id': self.env['stock.warehouse'].search([('name', '=', 'Home Guru Enterprises c/o neelam')], limit=1).lot_stock_id.id,
                    }))
                    print("OOOOOOOOOOOOOO", product_list)
                    print("pppppppppppppppp", line)
        loc = self.env['stock.warehouse'].search([('name', '=', 'Home Guru Enterprises c/o neelam')], limit=1).lot_stock_id
        stock_inventory_rec = self.env['stock.inventory'].sudo().create({
            'product_ids': [(6, 0, product_list)],
            'location_ids': [(6, 0, loc.ids)],
            #'accounting_date': datetime.now().date() - timedelta(days=38),
            'name': 'Home Stock',
            'line_ids': line
        })
        stock_inventory_rec.action_start()
        stock_inventory_rec.action_validate()

    def create_stock_sharma_general(self):
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        data = [sheet.row_values(rowx) for rowx in range(1, sheet.nrows)]
        line = []
        product_list = []
        for r in data:
            print("rrrrrrrrrrrrrrr", r[2])
            if r[0]:
                r[2] = str(r[2]).replace('.0', '')
                print("tttttttttttttt", r[2])
                product_rec = self.env['product.product'].search([('type', '=', 'product'), ('default_code', '=', r[2])])
                if product_rec:
                    print("eeeeeeeeee", product_rec)
                    product_list.append(product_rec.id)
                    line.append((0, 0, {
                        'product_id': product_rec.id,
                        'product_qty': r[1] if r[1] else 0.0,
                        'location_id': self.env['stock.warehouse'].search([('name', '=', 'Sharma General Store (600002)')], limit=1).lot_stock_id.id,
                    }))
                    print("OOOOOOOOOOOOOO", product_list)
                    print("pppppppppppppppp", line)
        loc = self.env['stock.warehouse'].search([('name', '=', 'Sharma General Store (600002)')], limit=1).lot_stock_id
        stock_inventory_rec = self.env['stock.inventory'].sudo().create({
            'product_ids': [(6, 0, product_list)],
            'location_ids': [(6, 0, loc.ids)],
            #'accounting_date': datetime.now().date() - timedelta(days=38),
            'name': 'Sharm Stock',
            'line_ids': line
        })
        stock_inventory_rec.action_start()
        stock_inventory_rec.action_validate()

    def create_stock_parth_super_store(self):
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        data = [sheet.row_values(rowx) for rowx in range(1, sheet.nrows)]
        line = []
        product_list = []
        for r in data:
            print("rrrrrrrrrrrrrrr", r[2])
            if r[0]:
                r[2] = str(r[2]).replace('.0', '')
                print("tttttttttttttt", r[2])
                product_rec = self.env['product.product'].search([('type', '=', 'product'), ('default_code', '=', r[2])])
                if product_rec:
                    print("eeeeeeeeee", product_rec)
                    product_list.append(product_rec.id)
                    line.append((0, 0, {
                        'product_id': product_rec.id,
                        'product_qty': r[1] if r[1] else 0.0,
                        'location_id': self.env['stock.warehouse'].search([('name', '=', 'Parth Super store (600104)')], limit=1).lot_stock_id.id,
                    }))
                    print("OOOOOOOOOOOOOO", product_list)
                    print("pppppppppppppppp", line)
        loc = self.env['stock.warehouse'].search([('name', '=', 'Parth Super store (600104)')], limit=1).lot_stock_id
        stock_inventory_rec = self.env['stock.inventory'].sudo().create({
            'product_ids': [(6, 0, product_list)],
            'location_ids': [(6, 0, loc.ids)],
            #'accounting_date': datetime.now().date() - timedelta(days=38),
            'name': 'Parth Super Store Stock',
            'line_ids': line
        })
        stock_inventory_rec.action_start()
        stock_inventory_rec.action_validate()

    def create_stock_rozana_mart(self):
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        data = [sheet.row_values(rowx) for rowx in range(1, sheet.nrows)]
        line = []
        product_list = []
        for r in data:
            print("rrrrrrrrrrrrrrr", r[2])
            if r[0]:
                r[2] = str(r[2]).replace('.0', '')
                print("tttttttttttttt", r[2])
                product_rec = self.env['product.product'].search([('type', '=', 'product'), ('default_code', '=', r[2]), ('name', '=', r[0])])
                if product_rec:
                    print("eeeeeeeeee", product_rec)
                    product_list.append(product_rec.id)
                    line.append((0, 0, {
                        'product_id': product_rec.id,
                        'product_qty': r[1] if r[1] else 0.0,
                        'location_id': self.env['stock.warehouse'].search([('name', '=', 'Rozana Mart C/O Ishank Goel (600144)')], limit=1).lot_stock_id.id,
                    }))
                    print("OOOOOOOOOOOOOO", product_list)
                    print("pppppppppppppppp", line)
        loc = self.env['stock.warehouse'].search([('name', '=', 'Rozana Mart C/O Ishank Goel (600144)')], limit=1).lot_stock_id
        stock_inventory_rec = self.env['stock.inventory'].sudo().create({
            'product_ids': [(6, 0, product_list)],
            'location_ids': [(6, 0, loc.ids)],
            #'accounting_date': datetime.now().date() - timedelta(days=38),
            'name': 'Rozana Stock',
            'line_ids': line
        })
        stock_inventory_rec.action_start()
        stock_inventory_rec.action_validate()