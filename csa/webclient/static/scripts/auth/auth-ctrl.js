'use strict';

angular.module('csa')
    .controller('AuthCtrl', function ($scope, $location, Auth) {
        $scope.errorMessage   = null;
        var getCredentials    = function () {
            return {
                username: $scope.username,
                password: $scope.password
            };
        };
        // display error message on failed login
        var onError           = function (response) {
            if (typeof response.data == 'string') {
                $scope.errorMessage = response.data;
            } else {
                $scope.errorMessage = response.data.detail;
            }
            /*Auth.setCurrentUser(null);*/
        };
        $scope.login          = function () {
            Auth.login(getCredentials()).then(function (response) {
                // login successful
                $scope.errorMessage = null;
                $location.path('/');
                Auth.setCurrentUser(response.data, $scope.remember);
            }, onError);
        };
        $scope.logout         = function () {
            Auth.logout().then(function (response) {
                // login successful
                $scope.errorMessage = null;
                $location.path('/');
                Auth.setCurrentUser(null, $scope.remember);
                Auth.cancelAllIntervals();
            }, onError);
        };
        $scope.getCurrentUser = function () {
            return Auth.getCurrentUser();
        };
    });