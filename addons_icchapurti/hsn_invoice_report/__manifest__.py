# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "HSN Invoice Report",

    'summary': """HSN based grouping of Products in Invoice""",

    'description': """
        This module adds a functionality for HSN based grouping of Products in Invoice.
    """,

    'license': 'AGPL-3',

    'author': "FOSS INFOTECH PVT LTD",

    'live_test_url': 'https://www.youtube.com/watch?v=uMRBBx0iBw8',

    'website': "http://www.fossinfotech.com",

    'category': 'Accounting',

    'version': '14.0.1',

    'depends': ['sale', 'account', 'l10n_in', 'purchase', 'purchase_enhancement'],

    'data': [
        'report/reports.xml',
        'report/invoice_report_template.xml',
        'report/purchase_order_templates.xml',
        'report/picking_operation_report.xml',
        'report/sale_report_templates.xml',
        'report/layout.xml',
        'view/account_move_inherit.xml'
    ],

    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/index.html',
    ],

    'installable': True,

    'auto_install': False,

    'application': True,

}
