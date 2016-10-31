$(document).ready(function() {
    var socket = io('http://' + document.domain + '/socketio');

    socket.on('my response', function() {
        invoice_table.ajax.reload( null, false );
    });

    var invoice_table = $('#invoice_table').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/inventory/invoices/ajax',
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
                    return '<a href="/inventory/invoices/' + data + '/">' + data + '</a>';
                }
            },

            {
                data: "received_date",
                responsivePriority: 2
            },

            {
                data: "received_date",
                responsivePriority: 5,
                className: "text-center",
                render: function ( data, type, row ) {
                    return '<small>Pending</small>';
                }
            },

            {
                responsivePriority: 3,
                className: "text-center",
                render: function (data, type, row) {
                  return row.parts.length;
                },
            },

            {
                data: "received_date",
                responsivePriority: 4,
                className: "text-center",
                render: function ( data, type, row ) {
                    return '<small>Pending</small>';
                }
            }
        ],
        "pageLength": 30,
        "lengthChange": false
    });

    $(window).scroll(function(){
        $(".paginate_button > a").blur();
    });
});
