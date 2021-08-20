# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "GST E-Way Bill",
  "summary"              :  """GST Ewaybill""",
  "category"             :  "website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-GST-Ewaybill.html",
  "description"          :  """This module works very well with latest version of Odoo 13.0
--------------------------------------------------------------""",
  "live_test_url"        :  "http://odoo.webkul.com:8010/web?db=gst_db#action=393&model=sale.order&view_type=list&menu_id=251",
  "depends"              :  [
                             'l10n_in',
                             'sale_stock',
                             'wk_wizard_messages',
                            ],
  "data"                 :  [
                             'security/ewaybill_security.xml',
                             'security/ir.model.access.csv',
                             'data/data_unit_quantity.xml',
                             'data/ewaybill_server_actions.xml',
                             'wizard/consolidated_ewaybill_view.xml',
                             'wizard/vehicle_no_updation_view.xml',
                             'views/ewaybill_uqc_view.xml',
                             'views/ewaybill_transporter_view.xml',
                             'views/gst_ewaybill_action_view.xml',
                             'views/res_config_view.xml',
                             'views/gst_ewaybill_menu_view.xml',
                             'views/sale_views.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}