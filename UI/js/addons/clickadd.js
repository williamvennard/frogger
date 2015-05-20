var Note = function($scope){
        $scope.items = [];

        $scope.add = function () {
          $scope.items.push({ });
        };
        $scope.remove = function(index) { 
            $scope.items.splice(index, 1);
        };
}