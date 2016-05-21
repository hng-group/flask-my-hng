$(document).ready(function(){
    $("#new_invoice_form").validate({
        rules: {
            password: {
                 required: true,
                 minlength: 3
            },
            url: {
                 required: true,
                 url: true
            },
            invoice_number: {
                 required: true,
                 digits: true,
                 minlength: 10,
                 maxlength: 10
            },
            date_received: {
                 required: true,
                 date: true
            },
            max: {
                 required: true,
                 maxlength: 4
            }
        }
    });

    
    $('#start_date').datepicker({
        todayBtn: "linked",
        keyboardNavigation: true,
        forceParse: false,
        calendarWeeks: true,
        autoclose: true
    });
    $('#start_date').datepicker('setDate', 'today')
});