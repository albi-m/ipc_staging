{
    'name': 'Approve Orders',
    'version': '14.0.0.0.0',
    'description': """""",
    'summary': 'Approve Orders',
    'category': 'tools',
    'author': 'Cybrosys Technologies',
    'depends': ['stock', 'purchase'],
    'data': [
        'views/stock_move_line.xml',
        'views/purchase_order.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
