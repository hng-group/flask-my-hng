$(document).ready(function() {

    var stock_inv = $('#stock_inv').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/inventory/parts/ajax',
            dataSrc: ''
        },
        "deferRender": true,
        "stateSave": true,
        "columns": [
            {
                data: "part_number",
                responsivePriority: 1,
                render: function ( data, type, row ) {
                    return '<a href="/inventory/parts/' + data + '/">' + data + '</a>';
                }
            },

            {
                data: "description",
                responsivePriority: 3
            },

            {
                data: "machine_type",
                responsivePriority: 7,
                className: "machine-type"
            },

            {
                data: "price",
                responsivePriority: 6,
                className: "asc-price"
            },

            {
                data: 'invoices',
                responsivePriority: 4,
                className: "claimable",
                render: function (invoices, type, part) {
                  var display;
                  var claimable = invoices.filter(function(invoice) {
                      return [
                        'New',
                      ].indexOf(invoice.status) >= 0;
                  });
                  if (claimable.length >= 1) {
                    display = '<span class="fa fa-check"></span>';
                  } else {
                    display = '<span class="fa fa-times"></span>';
                  }
                  return display;
                }
            },

            {
                responsivePriority: 5,
                className: "stock-quantity",
                render: function(data, type, part) {
                  var stock_invoices = part.invoices.filter(function(invoice) {
                      return [
                        'New',
                        'In Stock - Claimed'
                      ].indexOf(invoice.status) >= 0;
                  });
                  return stock_invoices.length;
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
                  display = '<a class="part-reserve"><i class="fa fa-circle-o-notch"></i></a> &nbsp;<span class="label label-green btn-rounded">In stock</span>';
                } else if (stock_invoices.length >= 1 && stock_invoices.length < 3) {
                  display = '<a class="part-reserve"><i class="fa fa-circle-o-notch"></i></a> &nbsp;<span class="label label-warning btn-rounded">Low stock</span>';
                } else {
                  display = '<a class="part-reserve"><i class="fa fa-circle-o-notch"></i></a> &nbsp;<span class="label label-danger btn-rounded">Out of stock</span>';
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
