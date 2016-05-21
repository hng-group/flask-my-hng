$(document).ready(function() {
    
    var completed_exam_table = $('#completed_exam_table').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/knowledge/exam/ajax/completed-exams',
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
                    return display = '<a href="/knowledge/exam/' + row.id + '/result/">' + row.name + '</a>';
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
                data: "taken_date",
                responsivePriority: 2,
                render: function ( data ) {
                    return display = '<b>Taken on: </b>' + data;
                }
            },

            {
                data: "score",
                responsivePriority: 4,
                className: 'text-right',
                render: function ( data ) {
                    return display = '<b>Score: </b>' + data;
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