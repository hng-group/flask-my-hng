$(document).ready(function() {
    $(document).on('click', '#get_shelf_report', function(e) {
      e.preventDefault();
      shelf_report_table.clear();
      var shelf = $('#shelf option:selected').val();
      $.post(window.location.pathname, {shelf: shelf}, function(parts) {
        shelf_report_table.rows.add(parts).draw();
        swal("Success!", "Get shelf report successfully!", "success");
      });
    });

    $(document).on('click', '#clear_table', function(e) {
      e.preventDefault();
      var table_data = [];
      shelf_report_table.clear();
      shelf_report_table.rows.add(table_data).draw();
    });

    var shelf_report_table = $('#shelf_report_table').DataTable({
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
                data: "invoice",
                responsivePriority: 1,
                render: function (invoice, type, row) {
                    return '<a href="/inventory/invoices/' + invoice.invoice_number+ '/">' + invoice.invoice_number + '</a>';
                }
            },

            {
                data: "part",
                responsivePriority: 2,
                render: function (part, type, row) {
                    return '<a href="/inventory/parts/' + part.part_number + '/">' + part.part_number + '</a>';
                }
            },

            {
                data: "part",
                responsivePriority: 3,
                render: function (part, type, row) {
                  return part.description;
                }
            },


            {
                data: "invoice",
                className: "text-center",
                responsivePriority: 4,
                render: function (invoice, type, row) {
                  return utils.toUSDate(invoice.received_date);
                }
            },

            {
                data: "claimed_date",
                className: "text-center",
                responsivePriority: 5
            },

            {
                data: "part",
                className: "text-center",
                responsivePriority: 6,
                render: function(part, type, row) {
                  return part.price;
                }
            },

            {
                data: "shelf_location",
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
