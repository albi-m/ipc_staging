{
'name': 'POS Receipt',
    'version': '14.0.2',
    'description': """ POS Receipt Custom""",
    'summary': 'Customised POS Receipt',
    'category': 'point_of_sale',
    'author':'Ichhapurti.com(Pavan)',
    'website':'',
    'last_updated':'17/06/2021',
    'depends': ['base', 'point_of_sale',],
    'data': ['views/pos_custom.xml',
             'views/pos_session_inherit.xml'],

    'demo': [],
    'qweb': ['static/src/xml/pos_custom_receipt.xml'],

    'installable': True,
    'application':True,
    'auto_install': False,
}