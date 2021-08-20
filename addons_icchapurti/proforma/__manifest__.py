{
'name': 'PRO Forma Report',
    'version': '14.0.0',
    'description': """ Print PRO FORMA Report """,
    'summary': 'Print PRO FORMA Report',
    'category': 'sales',
    'author':'Ichhapurti.com(Pavan)',
    'website':'',
    'last_updated':'22/07/2021',
    'depends': ['base', 'stock','product','sale' ],
    'data': ['report/proforma_report_view.xml',
             'report/proforma_report_template.xml',
             'views/sale_order_inherit.xml',
             'report/layout.xml'],

    'demo': [],
    'qweb': [],

    'installable': True,
    'application':True,
    'auto_install': False,
}