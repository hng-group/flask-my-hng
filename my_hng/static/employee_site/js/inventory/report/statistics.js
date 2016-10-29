$(document).ready(function() {
    function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
    var myjson = [];
    $.getJSON("/internal/inventory/report/ajax/statistics", function(data){
        myjson = data;
        var current_stock_inv_value = 0.00;
        var current_unclaimed_inv_value = 0.00;
        for (i = 0; i < myjson.length; i++) { 
            current_stock_inv_value += myjson[i][7];
            current_unclaimed_inv_value += myjson[i][8];
        }
        var current_claimed_inv_value = current_stock_inv_value - current_unclaimed_inv_value
        setTimeout(function(){
            $("#current_stock_inv_value").html('<h5>Current Stock Inventory Value</h5> <h1 class="no-margins">$&nbsp;' + numberWithCommas(current_stock_inv_value.toFixed(2)) + '</h1><div class="stat-percent font-bold text-navy">100%</i></div> <small>Percentage of Total Inventory</small>');
            $("#current_unclaimed_inv_value").html('<h5>Current Unclaimed Inventory Value</h5> <h1 class="no-margins">$&nbsp;' + numberWithCommas(current_unclaimed_inv_value.toFixed(2)) + '</h1><div class="stat-percent font-bold text-navy">??%</i></div> <small>Percentage of Total Inventory</small>');
            $("#current_claimed_inv_value").html('<h5>Current Claimed Inventory Value</h5> <h1 class="no-margins">$&nbsp;' + numberWithCommas(current_claimed_inv_value.toFixed(2)) + '</h1><div class="stat-percent font-bold text-navy">??%</i></div> <small>Percentage of Total Inventory</small>');
        }, 2000)
    });
});