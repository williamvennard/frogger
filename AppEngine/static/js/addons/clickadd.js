(function(angular) {
  'use strict';
angular.module('controller', [])
  .controller('SettingsController', ['$scope', SettingsController]);

function SettingsController($scope) {
  this.name = "";
  this.items = [];
}


SettingsController.prototype.addItem = function() {
  if (this.items.length < 4) {
    this.items.push({source: 'External', bandwidth: 20, delay: 2 });
  } else {
    this.removeItem(0);
  }
  console.log("addItem: this.items.length = ",this.items.length);
};


SettingsController.prototype.removeItem = function(index) {
  console.log("removeItem: index = ",index);
  console.log("removeItem: this.items[index] = ",this.items[index]);
  this.items.splice(index, 1);
  console.log("removeItem: this.items = ",this.items);
  for (var i = 0; i < this.items.length; i++) {
    console.log("i=",i);
    console.log(JSON.stringify(this.items[i], null, 4));
  }
};

SettingsController.prototype.sourceSelect = function(source) {
  var sourceSelect = document.getElementById('sourceSelect');
  j = 0;
  for (item in this.items) {
    if(item.source == source) {
      sourceSelect.selectedIndex = j;
      break;
    }
    j = j+1;
  }
};
})(window.angular);

  
