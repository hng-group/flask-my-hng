$(document).ready(function() {
    $("#add_part_button").click(function(e){
        e.preventDefault();
        $('#part_list').append('<tr> <input type="hidden" name="invoice_detail_id[]" class="form-control part_input" value="somerandomstringthatcantbeinvoicedetailid"> <td id="invoice_parts"> <input type="text" style="text-transform:uppercase" name="part_numbers[]" class="form-control part_input" placeholder="Part #" value=""> </td> <td> <input type="text" name="part_descriptions[]" class="form-control part_input" placeholder="Part description"> </td> <td> <input type="text" name="assoc_pos[]" class="form-control part_input" placeholder="Assoc. PO" value=""> </td> <td> <input type="text" name="part_prices[]" class="form-control part_input" placeholder=""> </td> <td> <input type="text" name="locations[]" class="form-control part_input" placeholder="" value=""> </td> <td> <select name="statuses[]" class="form-control" > <option value="New" selected>New</option> <option value="Dispatched">Dispatched</option> <option value="In Stock - Claimed">In Stock - Claimed</option> <option value="Used - Claimed">Used - Claimed</option> <option value="5">Returned</option></select> </td> </tr>'); //add input box
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
