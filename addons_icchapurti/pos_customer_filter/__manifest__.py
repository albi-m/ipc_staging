{
	"name": "POS Customer Filter",
	"version": "14.0.1",
	'description': """ Filter customer data and doesnot display companies in POS Customer List""",
    'summary': 'Customised Customer Filter',
	"sequence": 5,
	'author':'Ichhapurti.com',
	'website':'www.ichhapurti.com',
	"depends": ["base","point_of_sale"],
	"category": "point_of_sale",
	"data": ['views/assets.xml',],
	"demo": [],
	'qweb': [
		# 'static/src/xml/pos_customer_view.xml',
	],
	"auto_install": False,
	"installable": True,
	"application": True,
}
