$(document).ready(function() {
    var socket = io('http://' + document.domain + '/socketio');

    socket.on('shelf report data', function(json) {
        var table_data = JSON.parse(json);
        shelf_report_table.rows.add(table_data).draw();
        swal("Success!", "Get shelf report successfully!", "success");
    });

    $(document).on('click', '#get_shelf_report', function() {
        shelf_report_table.clear();
        socket.emit('shelf report', {shelf: $('#shelf option:selected').val()});
    });

    $(document).on('click', '#clear_table', function() {
        var table_data = [];
        shelf_report_table.clear();
        shelf_report_table.rows.add(table_data).draw();
    });

    var shelf_report_table = $('#shelf_report_table').DataTable( {
        "responsive": true,
        "autoFill": true,
        "data": [],
        "deferRender": true,
        "stateSave": true,
        "order": [[ 0, 'desc' ]],
        "dom": 'frtBip',
        "buttons": [
           'excel', 'pdf', 'print'
        ],
        "columns": [
            {
                data: "invoice_number",
                responsivePriority: 1,
                render: function ( data, type, row ) {
                    return display = '<a href="/internal/inventory/invoices/' + data + '/view/">' + data + '</a>';
                }
            },

            {
                data: "part_number",
                responsivePriority: 2,
                render: function ( data, type, row ) {
                    return display = '<a href="/internal/inventory/stock-inventory/' + data + '/view/">' + data + '</a>';
                }
            },

            {
                data: "part_description",
                responsivePriority: 3
            },


            {
                data: "received_date",
                className: "text-center",
                responsivePriority: 4
            },

            {
                data: "claimed_date",
                className: "text-center",
                responsivePriority: 5
            },

            {
                data: "part_price",
                className: "text-center",
                responsivePriority: 6
            },

            {
                data: "location",
                className: "text-center",
                responsivePriority: 7
            },

            {
                data: "status",
                className: "text-center",
                responsivePriority: 8
            }
        ],
        "pageLength": 15
    });
    $(window).scroll(function(){
        $(".paginate_button > a").blur();
    });
});