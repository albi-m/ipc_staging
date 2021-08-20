{
    'name': 'Purchase Enhancements',
    'version': '14.0.5',
    'description': """ """,
    'summary': '',
    'category': 'purchase',
    'author':'Ichhapurti.com(Pavan)',
    'website':'',
    'last_updated':'10/08/2021',
    'depends': ['base', 'purchase', 'account','sale','stock','barcode_update'],
    'data': [
            'views/purchase_custom_view.xml',
            'views/account_move_view.xml',
            'report/purchase_order_templates.xml',
            'report/report_invoice.xml',
            'views/res_partner_custom_view.xml',
            'views/sale_order_custom_view.xml',
            'views/stock.xml',
    ],
    'demo': [],
    'installable': True,
    'application':True,
    'auto_install': False,
}
