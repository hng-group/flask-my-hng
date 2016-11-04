(function(module) {
  'use strict';
  var utils = {};

  utils.toUSDate = function (string) {
    var date = string.split('-');
    if (date.length === 3) {
      return date[1] + '/' + date[2] + '/' + date[0];
    }
  };


  module.utils = utils;
}(window));
