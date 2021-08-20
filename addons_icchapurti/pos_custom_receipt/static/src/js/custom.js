odoo.define('pos_custom_receipt.custom', function (require) {
"use strict";


var models = require('point_of_sale.models');


var _super_ordermodel = models.Order.prototype;

models.Order = models.Order.extend({
    export_for_printing: function() {
        var receipt = _super_ordermodel.export_for_printing.apply(this,arguments);
        var i;
        var k = 0;
        models = this.orderlines.models;
        for (i=0; i < models.length; i++){
            k =k + models[i].quantity;
        }
        receipt.tot_pos_qty = k
        return receipt;

    },
});


});
