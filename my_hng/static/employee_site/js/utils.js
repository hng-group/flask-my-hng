(function(module) {
  'use strict';
  var utils = {};

  utils.toUSDate = function (string) {
    if (typeof(string) === 'string') {
      var date = string.split('-');
      if (date.length === 3) {
        return date[1] + '/' + date[2] + '/' + date[0];
      }
    } else {
      return string;
    }
  };


  module.utils = utils;
}(window));
