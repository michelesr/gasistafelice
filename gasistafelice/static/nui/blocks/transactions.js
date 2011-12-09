
jQuery.UIBlockAccTransactsList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("transactions", "table");
    },
        //this.active_view = "edit_multiple";
        //this.default_view = this.active_view;

    rendering_table_post_load_handler: function() {

        var block_obj = this;
        // Init dataTables

//        0: 'pk',
//        1: 'date',
//        2: 'issuer',
//        3: 'source',
//        4: 'kind',
//        5: 'description',
//        6: 'is_confirmed'

        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers',
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    {"bSearchable":true,"bSortable":true,"sWidth":"5%","bVisible": true},
                    {"bSearchable":false,"bSortable":false,"sWidth":"20%",},
                    {"bSearchable":false,"bSortable":false,"sWidth":"10%"},
                    {"bSearchable":false,"bSortable":false,"sWidth":"40%"},
                    {"bSearchable":false,"bSortable":false,"sWidth":"5%","sClass":"taright"}
                ]
            });

        return this._super();

    }

});

jQuery.BLOCKS["transactions"] = new jQuery.UIBlockAccTransactsList();
