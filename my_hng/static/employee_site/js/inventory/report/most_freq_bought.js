$(document).ready(function() {

    var most_freq_bought = $('#most_freq_bought').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/inventory/report/ajax/top-50-part',
            dataSrc: ''
        },
        "deferRender": true,
        "order": [[ 3, 'desc' ]],
        "scrollY": "525px",
        "ordering": false,
        "columns": [
            {
                data: 'part_number',
                responsivePriority: 1,
                render: function ( data, type, row ) {
                    return display = '<a href="/inventory/parts/' + data + '/">' + data + '</a>';
                }
            },

            {
                data: 'description',
                responsivePriority: 3
            },

            {
                data: 'machine_type',
                responsivePriority: 7,
                className: "text-center"
            },


            {
                data: 'invoices',
                responsivePriority: 5,
                className: "amount-bought",
                render: function(data, type, row) {
                  return data.length;
                }
            },
            {
                data: 'invoices',
                responsivePriority: 2,
                className: "stock-status",
                render: function (invoices, type, row) {
                  var stock_invoices = invoices.filter(function(invoice) {
                      return [
                        'New',
                        'In Stock - Claimed'
                      ].indexOf(invoice.status) >= 0;
                  });
                  var display;
                  if (stock_invoices.length >= 3) {
                    display = '<span class="label label-green btn-rounded">In stock</span>';
                  } else if (stock_invoices.length >= 1 && stock_invoices.length < 3) {
                    display = '<span class="label label-warning btn-rounded">Low stock</span>';
                  } else {
                    display = '<span class="label label-danger btn-rounded">Out of stock</span>';
                  }
                  return display;
                }
            }
        ],
        "pageLength": 15,
        "lengthChange": false
    });

    $(window).scroll(function(){
        $(".paginate_button > a").blur();
    });


});
