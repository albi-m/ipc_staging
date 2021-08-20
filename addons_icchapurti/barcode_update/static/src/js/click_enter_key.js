odoo.define('barcode_update.SubmitEnter', function(require){
    'use strict';

    $(document).ready(function(){
        $("body").on("keyup", 'input', function(e){
             var key = e.keyCode;
             if(key == 13)
              {
                $('#click_sim').trigger('click');
                return true;
              }
        });
    });
});