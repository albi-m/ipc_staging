{
    'name': 'Inter Company Sale to Purchase || Sale to Purchase auto Create multi Company',
    'category': 'Extra-Tootls',
    'summary': 'Using this module you can auto create purchase order on Sale Confirmation and Invoice Creation in another Company',
    'description': """ Using this module you can auto create purchase order on Sale Confirmation and Invoice Creation in another Company """,
    'price': 25,
    'version': '14.1.1.1',
    'currency': 'EUR',
    "author" : "MAISOLUTIONSLLC",
    'sequence': 1,
    "email": 'apps@maisolutionsllc.com',
    "website":'http://maisolutionsllc.com/',
    'license': 'OPL-1',
    'depends': ['purchase', 'sale_stock', 'sale_management'],
    'data': [
        'views/res_company_view.xml',
    ],
    "live_test_url" : "https://youtu.be/QQyK_WgwLdc",
    'demo': [],
    'test': [],
    'images': ['static/description/main_screenshot.png'],    
    'installable': True,
    'auto_install': False,
}
