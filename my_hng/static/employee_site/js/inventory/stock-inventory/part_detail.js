$(document).ready(function() {
    var part_invoice_table = $('#part_invoice_table').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/internal/inventory/stock-inventory/' + part_number + '/view/ajax/stock-status',
            dataSrc: ''
        },
        "deferRender": true,
        "stateSave": true,
        "order": [[ 0, 'desc' ]],
        "columns": [
            {
                data: "invoice_number",
                responsivePriority: 1,
                render: function ( data, type, row ) {
                    return display = '<a href="/internal/inventory/invoices/' + data + '/view/">' + data + '</a>';
                }
            },

            {
                data: "assoc_po",
                responsivePriority: 2
            },

            {
                data: "location",
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