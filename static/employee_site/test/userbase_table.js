$(document).ready(function() {
    
    var user_table = $('#user_table').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/internal/inventory/invoices/ajax',
            dataSrc: ''
        },
        buttons: [
            'copy', 'excel', 'pdf'
        ],
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
        "pageLength": 10,
        "lengthChange": false
    });
    
    $(window).scroll(function(){
        $(".paginate_button > a").blur();
    });
    setInterval(function(){
      user_table.ajax.reload(null, false);
    }, 30000);
    
});