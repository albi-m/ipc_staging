{
'name': 'Update Inventory By Barcode',
    'version': '14.0.2',
    'description': """ Update Inventory By Barcode""",
    'summary': 'Update Inventory By Barcode',
    'category': 'stock',
    'author':'Ichhapurti.com(Pavan)',
    'website':'',
    'last_updated':'03/08/2021',
    'depends': ['base', 'stock','product' ],
    'data': [
        'views/stock_picking_custom_inherit.xml',
        'views/stock_picking.xml',
        'views/assets.xml'
    ],

    'demo': [],
    'qweb': [],

    'installable': True,
    'application':True,
    'auto_install': False,
}
