odoo.define('pos_custom_productlist.ProductItem', function(require) {
    'use strict';

    const ProductItem = require('point_of_sale.ProductItem');
    const Registries = require('point_of_sale.Registries');
    var models = require('point_of_sale.models');
    models.load_fields('product.product', ['mrp']);

    const CustomProductItem = ProductItem =>
        class extends ProductItem {
            get pdt_mrp() {
            const formattedMrp = this.env.pos.format_currency(this.props.product.mrp,'Product MRP');
            return formattedMrp;
        }
        };

    Registries.Component.extend(ProductItem, CustomProductItem);

    return ProductItem;
});
