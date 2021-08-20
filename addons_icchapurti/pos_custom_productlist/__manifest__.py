{
'name': 'POS Custom Product List',
    'version': '14.0.1',
    'description': """Shows MRP in the POS Product list""",
    'summary': 'Customised POS Product list View',
    'category': 'point_of_sale',
    'author':'Ichhapurti.com(Anand)',
    'website':'',
    'depends': ['point_of_sale','product_enhancement'],
    'data': [
             'views/pos_custom_assets.xml'
             ],
    'qweb': ['static/src/xml/pos_custom_pdt_list.xml'],
    'installable': True,
    'application':True,
    'auto_install': False,
}
