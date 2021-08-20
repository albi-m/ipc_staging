{
    'name': 'Import Sales Order Lines',
    'version': '14.0.1.0.0',
    'description': """""",
    'summary': 'Import Sales Order Lines',
    'category': 'tools',
    'author': 'Cybrosys Technologies',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_so.xml',
        'views/sale_order.xml'
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}