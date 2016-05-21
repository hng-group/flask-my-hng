$(document).ready(function() {
    var socket = io('http://' + document.domain + '/socketio');
    var role_table = $('#role_table').DataTable( {
        "responsive": true,
        "ajax": {
            url: '/admin/user-base/ajax/all-roles',
            dataSrc: ''
        },
        "searching": false,
        "deferRender": true,
        "stateSave": true,
        "order": [[ 0, 'desc' ]],
        "columns": [
            {
                data: "name",
                responsivePriority: 1
            },

            {
                data: "description",
                responsivePriority: 2
            },

            {
                data: "name",
                orderable: false,
                responsivePriority: 4,
                className: "text-center",
                render: function ( data, type, row ) {
                    return display = '<a href="#" type="button" id="' + data + '" class="delete_role btn btn-xs btn-danger"><i class="fa fa-times"></i></a>';
                }
            }
        ],
        "pageLength": 10,
        "lengthChange": false
    });
    
    $(window).scroll(function(){
        $(".paginate_button > a").blur();
    });
    

    var reset_new_role_form = $('#new_role_form').clone();
    $('#new_role_form').on('hidden.bs.modal', function(){ 
        $(this).replaceWith(reset_new_role_form);
    });
    socket.on('create role success', function(msg) {
        $("#process_add_role").html('<div class="alert alert-success" role="alert">' + msg.data + '</div>');
        $("button#create_new_role").prop('disabled', true);
        role_table.ajax.reload();
    });

    socket.on('create role error', function(msg) {
        $("#add_role_error_msg").html('<div class="alert alert-danger" role="alert">' + msg.data + '</div>');
    });

    $(document).on('click', 'button#create_new_role', function() {
        socket.emit('create role', {role: $('input#role').val(), role_description: $('input#role_description').val()});
    });

    $(document.body).on('click', '.delete_role' ,function(){
        var id = $(this).attr('id');
        sweetAlert(id);
        swal({
            title: "Are you sure?",
            text: "You will not be able to undo this action",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, delete it!",
            closeOnConfirm: false 
        }, 
        function(){
            socket.emit('delete role', {role: id});
        });
        
        socket.on('delete role error', function(msg) {
            swal("Cancelled", msg.data, "error");
        });

        socket.on('delete role success', function(msg) {
            role_table.ajax.reload();
            swal("Deleted!", "Role " + id + " has been deleted", "success");
        });
        
    });
});