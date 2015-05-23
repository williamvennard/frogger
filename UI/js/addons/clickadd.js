(function(angular) {
  'use strict';
angular.module('controller', [])
  .controller('SettingsController', ['$scope', SettingsController]);

function SettingsController($scope) {
  $scope.name = "";
  $scope.items = []
   


  $scope.add = function() {
    $scope.items.push({});
  };

  $scope.remove = function() {
    var index = $scope.items.indexOf();
    $scope.items.splice(index, 1);
  };

}
})(window.angular);