$(document).ready(function() {
    function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    function getPercentage(upper, lower) {
      return ((upper/lower) * 100).toFixed(2);
    }

    $.getJSON("/inventory/parts/ajax", function(parts){
        var current_stock_inv_value = 0.00;
        var current_unclaimed_inv_value = 0.00;
        var current_claimed_inv_value = 0.00;
        for (var i = 0; i < parts.length; i++) {
          parts[i].stock_qty = parts[i].invoices.filter(function(invoice){
            return [
              'New',
              'In Stock - Claimed'
            ].indexOf(invoice.status) >= 0;
          }).length;
          parts[i].unclaimed_qty = parts[i].invoices.filter(function(invoice){
            return [
              'New',
            ].indexOf(invoice.status) >= 0;
          }).length;
          parts[i].claimed_qty = parts[i].invoices.filter(function(invoice){
            return [
              'In Stock - Claimed'
            ].indexOf(invoice.status) >= 0;
          }).length;
          current_stock_inv_value += parts[i].stock_qty * parts[i].price;
          current_unclaimed_inv_value += parts[i].unclaimed_qty * parts[i].price;
          current_claimed_inv_value += parts[i].claimed_qty * parts[i].price;
        }
        $("#current_stock_inv_value").html('<h5>Current Stock Inventory Value</h5> <h1 class="no-margins">$&nbsp;' + numberWithCommas(current_stock_inv_value.toFixed(2)) + '</h1><div class="stat-percent font-bold text-navy">100%</i></div> <small>Percentage of Total Inventory</small>');
        $("#current_unclaimed_inv_value").html('<h5>Current Unclaimed Inventory Value</h5> <h1 class="no-margins">$&nbsp;' + numberWithCommas(current_unclaimed_inv_value.toFixed(2)) + '</h1><div class="stat-percent font-bold text-navy">' + getPercentage(current_unclaimed_inv_value, current_stock_inv_value) + '%</i></div> <small>Percentage of Total Inventory</small>');
        $("#current_claimed_inv_value").html('<h5>Current Claimed Inventory Value</h5> <h1 class="no-margins">$&nbsp;' + numberWithCommas(current_claimed_inv_value.toFixed(2)) + '</h1><div class="stat-percent font-bold text-navy">' + getPercentage(current_claimed_inv_value, current_stock_inv_value) + '%</i></div> <small>Percentage of Total Inventory</small>');
    });
});
