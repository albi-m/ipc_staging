{
    'name': 'Import Purchase Order Lines',
    'version': '14.0.2.0.0',
    'description': """""",
    'summary': 'Import Purchase Order Lines',
    'category': 'tools',
    'author': 'Cybrosys Technologies',
    'depends': ['purchase', 'purchase_enhancement'],
    'data': [
        'wizard/import_po.xml',
        'security/ir.model.access.csv',
        'views/purchase_order_line.xml'
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}