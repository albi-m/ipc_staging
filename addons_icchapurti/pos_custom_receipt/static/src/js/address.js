odoo.define('pos_custom_receipt.address', function (require) {
"use strict";

var models = require('point_of_sale.models');
models.load_fields('pos.config', ['name']);
models.load_fields('res.company', ['street', 'street2','city','state_id','zip','country_id'])

var _super_ordermodel = models.Order.prototype;

models.Order = models.Order.extend({
    export_for_printing: function() {
        var receipt = _super_ordermodel.export_for_printing.apply(this,arguments);
        receipt.pos_name = this.pos.config.name
        receipt.address_street = this.pos.company.street;
        receipt.address_street2 = this.pos.company.street2;
        receipt.address_city = this.pos.company.city;
        receipt.address_state_id = this.pos.company.state_id[1];
        receipt.address_zip = this.pos.company.zip;
        receipt.address_country_id = this.pos.company.country_id[1];
        console.log("HHHHHHHHHHH",receipt.address_state_id)
        return receipt;
    },
});


});
