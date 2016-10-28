$(document).ready(function() {
    
    var available_exam_table = $('#available_exam_table').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/knowledge/exam/ajax/all-exams',
            dataSrc: ''
        },
        "deferRender": true,
        "stateSave": true,
        "order": [[ 0, 'desc' ]],
        "language": {
          "emptyTable": "No test available"
        },
        "columns": [
            {
                data: "name",
                responsivePriority: 1,
                render: function ( data, type, row ) {
                    return display = '<a href="/knowledge/exam/' + row.id + '/view/">' + row.name + '</a>';
                }
            },

            {
                data: "description",
                responsivePriority: 2,
                render: function ( data ) {
                    return display = '<b>Description: </b>' + data;
                }
            },

            {
                data: "start_date",
                responsivePriority: 3,
                render: function ( data ) {
                    return display = '<b>Start: </b>' + data;
                }
            },

            {
                data: "end_date",
                responsivePriority: 4,
                render: function ( data ) {
                    return display = '<b>End: </b>' + data;
                }
            },

            {
                data: "limit_minutes",
                responsivePriority: 4,
                className: 'text-right',
                render: function ( data ) {
                    return display = '<b>Duration: </b>' + data + ' minutes';
                }
            },

        ],
        "pageLength": 30,
        "lengthChange": false
    });
    
    $(window).scroll(function(){
        $(".paginate_button > a").blur();
    });
    
});