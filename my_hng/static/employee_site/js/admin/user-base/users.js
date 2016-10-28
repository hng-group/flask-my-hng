$(document).ready(function() {
    
    var user_table = $('#user_table').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/admin/user-base/ajax/all-users',
            dataSrc: ''
        },
        "deferRender": true,
        "stateSave": true,
        "order": [[ 0, 'desc' ]],
        "columns": [
            {
                data: "last_name",
                responsivePriority: 1,
                render: function ( data, type, row ) {
                    return display = '<a href="/admin/user-base/' + row.id + '/view/">' + row.first_name + ' ' + row.last_name + '</a>';
                }
            },

            {
                data: "job_title",
                responsivePriority: 2
            },

            {
                data: "department",
                responsivePriority: 3
            },

            {
                data: "phone",
                responsivePriority: 4
            },

            {
                data: "email",
                responsivePriority: 4
            },


            {
                data: "city",
                responsivePriority: 5,
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
    
});