$(document).ready(function() {
    var max_fields      = 15; //maximum input boxes allowed
    var wrapper         = $("#part_list"); //Fields wrapper
    var add_button      = $("#add_part_button"); //Add button ID
    var x = 1; //initlal text box count
    $(add_button).click(function(e){ //on add input button click
        e.preventDefault();
        if(x < max_fields){ //max input box allowed
            x++; //text box increment
            $(wrapper).append('<tr> <input type="hidden" name="invoice_detail_id[]" class="form-control part_input" value="add"> <td id="invoice_parts"> <input type="text" style="text-transform:uppercase" name="part_numbers[]" class="form-control part_input" placeholder="Part #" value=""> </td> <td> <input type="text" name="part_descriptions[]" class="form-control part_input" placeholder="Part description"> </td> <td> <input type="text" name="assoc_pos[]" class="form-control part_input" placeholder="Assoc. PO" value=""> </td> <td> <input type="text" name="part_prices[]" class="form-control part_input" placeholder=""> </td> <td> <input type="text" name="locations[]" class="form-control part_input" placeholder="" value=""> </td> <td> <select name="statuses[]" class="form-control" > <option value="New" selected>New</option> <option value="Dispatched">Dispatched</option> <option value="In Stock - Claimed">In Stock - Claimed</option> <option value="Used - Claimed">Used - Claimed</option> <option value="5">Returned</option></select> </td> </tr>'); //add input box
        } else {

            alert("Only 15 additional parts are allowed");
        }
    });
    $('#date_received').datepicker({
        todayBtn: "linked",
        keyboardNavigation: true,
        forceParse: false,
        calendarWeeks: true,
        autoclose: true
    });

});

$(function() {
    enable_cb();
    $("#part_input").click(enable_cb);
});

function enable_cb() {
    $("input.part_input").prop("readonly", !this.checked);
}