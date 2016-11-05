$(document).ready(function() {
    var part_invoice_table = $('#part_invoice_table').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/inventory/parts/' + part_number + '/ajax',
            dataSrc: 'invoices'
        },
        "deferRender": true,
        "stateSave": true,
        "order": [[ 0, 'desc' ]],
        "columns": [
            {
                data: "invoice",
                responsivePriority: 1,
                render: function ( invoice, type, row ) {
                    return '<a href="/inventory/invoices/' + invoice.invoice_number+ '/">' + invoice.invoice_number + '</a>';
                }
            },

            {
                data: "purchase_order_number",
                responsivePriority: 2
            },

            {
                data: "shelf_location",
                responsivePriority: 3
            },

            {
                data: "claimed_date",
                responsivePriority: 3
            },

            {
                responsivePriority: 5,
                render: function ( data, type, row ) {
                    return display = '<small>Pending</small>';
                }
            },

            {
                data: "status",
                responsivePriority: 4
            }
        ],
        "pageLength": 15,
        "lengthChange": false
    });

    $(window).scroll(function(){
        $(".paginate_button > a").blur();
    });
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test/socketio');
    socket.on('my response', function() {
        invoice_table.ajax.reload( null, false );
    });

});
