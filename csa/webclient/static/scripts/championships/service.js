'use strict';

angular.module('csa')
  .service('Championships', function (settings, $http) {
    var ADDRESS = '/championship/championships/';
    return {
      all:      function () {
        return $http.get(settings.BASE_URL + ADDRESS);
      },
      get:      function (data, parameters) {
        parameters = typeof parameters !== 'undefined' ? parameters : {};
        return $http.get(settings.BASE_URL + ADDRESS + data + '/', {
          params: parameters
        });
      },
      query:    function (parameters) {
        parameters = typeof parameters !== 'undefined' ? parameters : {};
        return $http.get(settings.BASE_URL + ADDRESS, {
          params: parameters
        });
      },
      schedule: function (data) {
        return $http.post(settings.BASE_URL + '/championship/schedule/', data);
      }
    };
  });

angular.module('csa')
  .service('Teams', function (settings, $http) {
    var ADDRESS = '/championship/teams/';
    return {
      query: function (parameters) {
        parameters = typeof parameters !== 'undefined' ? parameters : {};
        return $http.get(settings.BASE_URL + ADDRESS, {
          params: parameters
        });
      }
    };
  });

angular.module('csa')
  .service('Groups', function (settings, $http) {
    var ADDRESS = '/championship/groups/';
    return {
      all:   function () {
        return $http.get(settings.BASE_URL + ADDRESS);
      },
      query: function (parameters) {
        parameters = typeof parameters !== 'undefined' ? parameters : {};
        return $http.get(settings.BASE_URL + ADDRESS, {
          params: parameters
        });
      }
    };
  });

angular.module('csa')
  .service('Participates', function (settings, $http) {
    var ADDRESS = '/championship/participates/';
    return {
      query: function (parameters) {
        parameters = typeof parameters !== 'undefined' ? parameters : {};
        return $http.get(settings.BASE_URL + ADDRESS, {
          params: parameters
        });
      }
    };
  });

angular.module('csa')
  .service('Matches', function (settings, $http) {
    var ADDRESS = '/championship/matches/';
    return {
      all:   function () {
        return $http.get(settings.BASE_URL + ADDRESS);
      },
      get:   function (data, parameters) {
        parameters = typeof parameters !== 'undefined' ? parameters : {};
        return $http.get(settings.BASE_URL + ADDRESS + data + '/', {
          params: parameters
        });
      },
      query: function (parameters) {
        parameters = typeof parameters !== 'undefined' ? parameters : {};
        return $http.get(settings.BASE_URL + ADDRESS, {
          params: parameters
        });
      }
    };
  });

angular.module('csa')
  .service('Results', function (settings, $http) {
    var ADDRESS = '/championship/results/';
    return {
      get:   function (data, parameters) {
        parameters = typeof parameters !== 'undefined' ? parameters : {};
        return $http.get(settings.BASE_URL + ADDRESS + data + '/', {
          params: parameters
        });
      },
      query: function (parameters) {
        parameters = typeof parameters !== 'undefined' ? parameters : {};
        return $http.get(settings.BASE_URL + ADDRESS, {
          params: parameters
        });
      }
    };
  });
