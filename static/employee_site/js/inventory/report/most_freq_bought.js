$(document).ready(function() {
    
    var most_freq_bought = $('#most_freq_bought').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/internal/inventory/report/ajax/top-50-part',
            dataSrc: ''
        },
        "deferRender": true,
        "order": [[ 3, 'desc' ]],
        "scrollY": "525px",
        "ordering": false,
        "columns": [
            {
                data: 0,
                responsivePriority: 1,
                render: function ( data, type, row ) {
                    return display = '<a href="/internal/inventory/stock-inventory/' + data + '/view/">' + data + '</a>';
                }
            },

            {
                data: 1,
                responsivePriority: 3
            },

            {
                data: 2,
                responsivePriority: 7,
                className: "text-center"
            },


            {
                data: 8,
                responsivePriority: 5,
                className: "amount-bought"
            },
            {
                data: 6,
                responsivePriority: 2,
                className: "stock-status",
                render: function ( data, type, row ) {
                    if (data >= 3) {
                        var display = '<span class="label label-primary btn-rounded">In stock</span>';
                        return display;
                    } else if (data >= 1 && data < 3) {
                        var display = '<span class="label label-warning btn-rounded">Low stock</span>';
                        return display;
                    } else {
                        var display = '<span class="label label-danger btn-rounded">Out of stock</span>';
                        return display;
                    }
                    
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