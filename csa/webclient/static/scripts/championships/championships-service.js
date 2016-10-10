'use strict';

angular.module('csa')
    .service('Championships', function (settings, $http) {
        var ADDRESS = '/championship/championships/';
        return {
            get:    function (data, parameters) {
                parameters = typeof parameters !== 'undefined' ? parameters : {};
                return $http.get(settings.BASE_URL + ADDRESS + data + '/', {
                    params: parameters
                });
            },
            query:  function (parameters) {
                parameters = typeof parameters !== 'undefined' ? parameters : {};
                return $http.get(settings.BASE_URL + ADDRESS, {
                    params: parameters
                });
            },
            save:   function (data) {
                return $http.post(settings.BASE_URL + ADDRESS, data);
            },
            patch:  function (data) {
                return $http.patch(settings.BASE_URL + ADDRESS +
                    getIdFromUrl(data.url) + '/', data);
            },
            remove: function (data) {
                return $http.delete(settings.BASE_URL + ADDRESS + data + '/');
            },
            schedule: function(data) {
                return $http.post(settings.BASE_URL + '/championship/schedule/', data);
            }
        };
    });

angular.module('csa')
    .service('Teams', function (settings, $http) {
        var ADDRESS = '/championship/teams/';
        return {
            get:    function (data, parameters) {
                parameters = typeof parameters !== 'undefined' ? parameters : {};
                return $http.get(settings.BASE_URL + ADDRESS + data + '/', {
                    params: parameters
                });
            },
            query:  function (parameters) {
                parameters = typeof parameters !== 'undefined' ? parameters : {};
                return $http.get(settings.BASE_URL + ADDRESS, {
                    params: parameters
                });
            },
            save:   function (data) {
                return $http.post(settings.BASE_URL + ADDRESS, data);
            },
            patch:  function (data) {
                return $http.patch(settings.BASE_URL + ADDRESS +
                    getIdFromUrl(data.url) + '/', data);
            },
            remove: function (data) {
                return $http.delete(settings.BASE_URL + ADDRESS + data + '/');
            }
        };
    });