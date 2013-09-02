function HomeCtrl($scope, $routeParams) {
}

function LabelCtrl($scope, $http) {
  //signup
  $scope.labelImageUrl = '';
  $scope.parcel = {};
  $scope.sending = false;

  $scope.createLabel = function() {
    $scope.sending = true;
    $scope.parcelErrorMessage = '';
    $http.post('/api/v1/parcel', $scope.parcel).
      success(function(data, status, headers, config) {
        $scope.parcel.length = '';
        $scope.parcel.width = '';
        $scope.parcel.height = '';
        $scope.parcel.weight = '';
        $scope.labelImageUrl = data.postageUrl;
        $scope.sending = false;
      }).
      error(function (data, status, headers, config) {
        $scope.sending = false;
        if (data.errorItem == 'parcel') {
          $scope.parcelErrorMessage = data.message;
        }
      });
  }

  $scope.resetLabel = function() {
    $scope.labelImageUrl = '';
  }
}
