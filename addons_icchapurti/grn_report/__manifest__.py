{
'name': 'GRN Report',
    'version': '14.0.1',
    'description': """ Print GRN Report """,
    'summary': 'Print GRN Report',
    'category': 'stock',
    'author':'Ichhapurti.com(Pavan)',
    'website':'',
    'last_updated':'29/07/2021',
    'depends': ['base', 'stock','product' ],
    'data': ['report/grn_report_view.xml',
             'report/grn_report_template.xml',
             'views/stock_picking_form.xml'],

    'demo': [],
    'qweb': [],

    'installable': True,
    'application':True,
    'auto_install': False,
}