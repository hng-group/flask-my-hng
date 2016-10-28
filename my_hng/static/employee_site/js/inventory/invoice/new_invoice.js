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
                 required: true
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

    
    $('#date_received').datepicker({
        todayBtn: "linked",
        keyboardNavigation: true,
        forceParse: false,
        calendarWeeks: true,
        autoclose: true
    });
    $('.new_invoice_date_received').datepicker('setDate', 'today')
});

$(document.body).on("input", ".part_number:last", function () {
    var x = 1;
    x++;
    $("#new_invoice_form .part_input").append('<wrapper><div class="row" id="part"> <div class="col-xs-5 col-sm-5"> <div class="form-group"> <label class="control-label" for="part_number' + x + '">Part Number</label> <input style="text-transform:uppercase" type="text" id="part_number' + x +'" name="part_numbers[]" value="" placeholder="Part #" class="form-control part_number" tabindex="'+ (x+2) +'"> </div> </div> <div class="col-xs-4 col-sm-4"> <div class="form-group"> <label class="control-label" for="assoc_po">Assoc. PO</label> <input type="text" id="assoc_po' + x + '" name="assoc_pos[]" value="" placeholder="PO #" class="form-control"> </div> </div> <div class="col-sm-2 hidden-xs"> <div class="form-group"> <label class="control-label" for="shelf_location">Shelf Location</label> <input type="text" id="shelf_location' + x + '" name="shelf_locations[]" value="" class="form-control"> </div> </div> <div class="col-xs-1"> <div class="form-group" style="margin-top: 22px;"> <div class="btn btn-white remove_field"><i class="fa fa-trash"></i> </div> </div> </div> </div> </wrapper>');
    $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault(); $(this).parentsUntil('wrapper').remove(); x--;
    })
});

$('body').on('keydown', 'input, select, textarea', function(e) {
    var self = $(this)
      , form = self.parents('form:eq(0)')
      , focusable
      , next
      ;
    if (e.keyCode == 13) {
        focusable = form.find('input,a,select,button,textarea').filter(':visible');
        next = focusable.eq(focusable.index(this)+1);
        if (next.length) {
            next.focus();
        } else {
            form.submit();
        }
        return false;
    }
});