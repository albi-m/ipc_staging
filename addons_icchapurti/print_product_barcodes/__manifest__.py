# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Print Product Barcodes",
    'summary': """Print Picking Barcodes""",
    'description': """
        This module adds a functionality for printing product barcodes.
    """,
    'license': 'AGPL-3',
    'author': "",
    'category': 'Stock',
    'version': '14.0.1',
    'depends': ['stock'],
    'data': [
        'report/product_barcode_template.xml',
        'report/packing_barcode_template.xml',
        'report/reports.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,

}
