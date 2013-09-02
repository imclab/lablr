angular.module('lablr')
  .factory('userSrv', function() {
    var userData = {
      userLoggedIn: false,
      username: ''
    };
    return userData;
  })
  .factory('apiSrv', ['$resource', function($resource) {
    var resources = {};
    resources.item = $resource('/api/v1/item/:itemId');
    return resources
  }])
;

