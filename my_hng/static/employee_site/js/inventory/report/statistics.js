$(document).ready(function() {
    function numberWithCommas(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    function getPercentage(upper, lower) {
      return ((upper/lower) * 100).toFixed(2);
    }

    $.getJSON("/inventory/report/ajax?type=stat", function(data) {
      var current_stock_inv_value = data.cur_total_val
      var current_unclaimed_inv_value = data.cur_unclaimed_val;
      var current_claimed_inv_value = data.cur_claimed_val;
      $("#current_stock_inv_value").html('<h5>Current Stock Inventory Value</h5> <h1 class="no-margins">$&nbsp;' + numberWithCommas(current_stock_inv_value.toFixed(2)) + '</h1><div class="stat-percent font-bold text-navy">100%</i></div> <small>Percentage of Total Inventory</small>');
      $("#current_unclaimed_inv_value").html('<h5>Current Unclaimed Inventory Value</h5> <h1 class="no-margins">$&nbsp;' + numberWithCommas(current_unclaimed_inv_value.toFixed(2)) + '</h1><div class="stat-percent font-bold text-navy">' + getPercentage(current_unclaimed_inv_value, current_stock_inv_value) + '%</i></div> <small>Percentage of Total Inventory</small>');
      $("#current_claimed_inv_value").html('<h5>Current Claimed Inventory Value</h5> <h1 class="no-margins">$&nbsp;' + numberWithCommas(current_claimed_inv_value.toFixed(2)) + '</h1><div class="stat-percent font-bold text-navy">' + getPercentage(current_claimed_inv_value, current_stock_inv_value) + '%</i></div> <small>Percentage of Total Inventory</small>');
    });
});
