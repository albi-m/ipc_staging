# -*- coding: utf-8 -*-
#################################################################################
# Author: GGJ Solutions (Ichhapurti)
# Copyright(c): 2021-Present GGJ Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
# You should have received a copy of the License along with this program.
#################################################################################
{
	"name"         : "Picking SLip",
	"summary"      : """Picking slip to display reserved and demnand quantity""",
	"category"     : "stock",
	"version"      : "14.0.4",
	"author"       : "GGJ Solutions (Ichhapurti)",
	"website"      : "https://www.ichhapurti.com/",
	"description"  : "Picking Slip",
	"depends": ['base', 'stock','product' ],
	"data"         : [
		'report/stock_report_views.xml',
		'report/report_pickingslip.xml',
		'report/report_packing_slip.xml',
		'report/report_dispatch_packing_slip.xml',
		'views/view_quant_package_form.xml',
	],
	"installable"  : True,
	"application"  : True,
    "auto_install" : False
}
