$(document).ready(function() {

    var client_table = $('#client_table').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/client/client-list/ajax/all-clients',
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
                    return display = '<a href="/client/client-list/' + row.id + '/view/">' + row.first_name + ' ' + row.last_name + '</a>';
                }
            },

            {
                responsivePriority: 2,
                render: function ( data, type, row ) {
                    return display = 'P: ' + row.phone.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3') + '<br>' + 'E: ' + row.email;
                }
            },

            {
                responsivePriority: 5,
                render: function ( data, type, row ) {
                    return display = row.address1 + ' ' + row.address2 + '<br>' + row.city + ', ' + row.state + ' ' + row.zip_code;
                }
            },

            {
                responsivePriority: 3,
                className: "text-center",
                render: function ( data, type, row ) {
                    var dateParts = row.added_date.split("-");
                    var usDate = dateParts[1] + '/' + dateParts[2] + '/' + dateParts[0];
                    return usDate;
                }
            },

            {
                data: "is_subscribed",
                responsivePriority: 4,
                className: "text-center",
                render: function ( data, type, row ) {
                    if (data === "T"){
                        return display = 'Yes';
                    } else if (data === "F") {
                        return display = "No"
                    }
                    
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