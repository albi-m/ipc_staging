odoo.define('pos_custom_receipt.custom_field', function (require) {
"use strict";

var models = require('point_of_sale.models');

//models.load_models([
//
//{
//model: 'pos.order',
//condition: function(self){ return true; },
//fields: ['text_amount_total'],
//domain: function(self){ return [['active','=',true]]; },
//loaded: function(self){ return true
//
//},
//}],{'after': 'product.product'});
//
//var _super_ordermodel = models.Order.prototype;
//
//models.Order = models.Order.extend({
//    export_for_printing: function() {
//        var receipt = _super_ordermodel.export_for_printing.apply(this,arguments);
//        receipt.text_amount_total = this.pos
//        console.log('JJJJJJJJJJ',this.get('env'))
//        return receipt;
//    },
//});
//});
