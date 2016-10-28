$(document).ready(function() {

    var article_table = $('#article_table').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/front-page/cms/ajax/allarticles',
            dataSrc: ''
        },
        "deferRender": true,
        "stateSave": true,
        "order": [[ 1, 'desc' ]],
        "columns": [
            {
                data: "title",
                responsivePriority: 1,
                render: function ( data, type, row ) {
                    return display = '<a href="/front-page/cms/' + row.id + '/edit/">' + data + '</a>';
                }
            },

            {
                data: "author_id",
                responsivePriority: 2

            },

            {
                data: "category",
                responsivePriority: 5
                // render: function ( data, type, row ) {
                //     return display = row.address1 + ' ' + row.address2 + '<br>' + row.city + ', ' + row.state + ' ' + row.zip_code;
                // }
            },

            {   
                responsivePriority: 3,
                className: "text-center",
                render: function ( data, type, row ) {
                    var addedDate = row.added_date.split("-");
                    var usDate = addedDate[1] + '/' + addedDate[2] + '/' + addedDate[0];
                    return usDate;
                }
            },

            {
                data: "status",
                responsivePriority: 4,
                className: "text-center"
            }
        ],
        "pageLength": 30,
        "lengthChange": false
    });
    
    $(window).scroll(function(){
        $(".paginate_button > a").blur();
    });
});