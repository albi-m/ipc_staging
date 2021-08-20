{
    'name': 'Add Purchase Vendor from PO',
    'version': '14.0.0.0.0',
    'description': """""",
    'summary': 'Add purchase vendor',
    'category': 'tools',
    'author': 'Cybrosys Technologies',
    'depends': ['purchase', 'product'],
    'data': [
        'views/purchase_order.xml',
        'wizard/assign_vendor.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
