$(document).ready(function() {
    
    var stock_inv = $('#stock_inv').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/internal/inventory/stock-inventory/ajax',
            dataSrc: ''
        },
        "deferRender": true,
        "stateSave": true,
        "columns": [
            {
                data: "part_number",
                responsivePriority: 1,
                render: function ( data, type, row ) {
                    return display = '<a href="/internal/inventory/stock-inventory/' + data + '/view/">' + data + '</a>';
                }
            },

            {
                data: "part_description",
                responsivePriority: 3
            },

            {
                data: "machine_type",
                responsivePriority: 7,
                className: "machine-type"
            },

            {
                data: "asc_price",
                responsivePriority: 6,
                className: "asc-price"
            },

            {
                data: "claimable_quanity",
                responsivePriority: 4,
                className: "claimable",
                render: function ( data, type, row ) {
                    if (data >= 1) {
                        var display = '<span class="fa fa-check"></span>';
                    } else {
                        var display = '<span class="fa fa-times"></span>';
                    }
                    return display;
                }
            },

            {
                data: "stock_quantity",
                responsivePriority: 5,
                className: "stock-quantity"
            },
            {
                data: "stock_quantity",
                responsivePriority: 2,
                className: "stock-status",
                render: function ( data, type, row ) {
                    if (data >= 3) {
                        var display = '<a class="part-reserve"><i class="fa fa-circle-o-notch"></i></a> &nbsp;<span class="label label-primary btn-rounded">In stock</span>';
                    } else if (data >= 1 && data < 3) {
                        var display = '<a class="part-reserve"><i class="fa fa-circle-o-notch"></i></a> &nbsp;<span class="label label-warning btn-rounded">Low stock</span>';
                    } else {
                        var display = '<a class="part-reserve"><i class="fa fa-circle-o-notch"></i></a> &nbsp;<span class="label label-danger btn-rounded">Out of stock</span>';
                    }
                    return display;
                    
                }
            }
        ],
        "pageLength": 30,
        "lengthChange": false
    });
    
    $(window).scroll(function(){
        $(".paginate_button > a").blur();
    });
    setInterval(function(){
      stock_inv.ajax.reload(null, false);
    }, 15000);
    
});