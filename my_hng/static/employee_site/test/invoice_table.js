$(document).ready(function() {
    
    var invoice_table = $('#invoice_table').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/internal/inventory/invoices/ajax',
            dataSrc: ''
        },
        "deferRender": true,
        "stateSave": true,
        "order": [[ 1, 'desc' ]],
        "columns": [
            {
                data: "invoice_number",
                responsivePriority: 1,
                render: function ( data, type, row ) {
                    return display = '<a href="/internal/inventory/invoices/' + data + '/view/">' + data + '</a>';
                }
            },

            {
                data: "date_received",
                responsivePriority: 2
            },

            {
                data: "date_received",
                responsivePriority: 5,
                className: "text-center",
                render: function ( data, type, row ) {
                    return display = '<small>Pending</small>';
                }
            },

            {
                data: "number_of_items",
                responsivePriority: 3,
                className: "text-center"
            },

            {
                data: "date_received",
                responsivePriority: 4,
                className: "text-center",
                render: function ( data, type, row ) {
                    return display = '<small>Pending</small>';
                }
            }
        ],
        "pageLength": 30,
        "lengthChange": false
    });
    
    $(window).scroll(function(){
        $(".paginate_button > a").blur();
    });
    
    // var socket = io.connect('http://' + document.domain + ':' + location.port + '/test/socketio');
    // socket.on('my response', function() {
    //     invoice_table.ajax.reload( null, false );
    // });
});