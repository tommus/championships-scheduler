'use strict';

angular.module('csa', ['ngRoute', 'ngCookies', 'ngStorage', 'angular-toasty', 'settings'])
    .factory('authInterceptor', ['$cookieStore', '$localStorage', '$location', 'settings', '$q',
        function ($cookieStore, $localStorage, $location, settings, $q) {
            return {
                response: function (response) {
                    if (!$cookieStore.get(settings.USER_LOGIN_ID_COOKIE) && !$localStorage.user)
                        $location.path('/login');
                    if (response.status === 403) {
                        return $q.reject(response);
                    }
                    else {
                        return $q.resolve(response)
                    }
                }
            }
        }])
    .config(function ($routeProvider, $httpProvider, settings) {
        $routeProvider
            .when('/', {
                templateUrl: settings.STATIC_URL + 'partials/dashboard/dashboard.html',
                controller:  'DashboardCtrl'
            })
            .when('/login', {
                templateUrl: 'static/partials/auth/login.html',
                controller:  'AuthCtrl'
            })
            .when('/logout', {
                templateUrl: 'static/partials/auth/login.html',
                controller:  'AuthCtrl'
            })
            .otherwise({
                redirectTo: '/'
            });

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        $httpProvider.interceptors.push([
            '$q', '$location', 'toasty', function ($q, $location, toasty) {
                return {
                    responseError: function (rejection) {
                        if (rejection.status === 403) {
                            // show error message for Forbidden
                            toasty.error({
                                title:        'Error 403',
                                msg:          'Forbidden',
                                showClose:    false,
                                clickToClose: true,
                                timeout:      5000
                            });
                            // mark session as not authenticated
                            // Auth.authenticated(false);
                            $location.path('/login');
                        }
                        if (rejection.status === 401) {
                            $location.path('/login');
                        }
                        return $q.reject(rejection);
                    }
                }
            }
        ]);

        $httpProvider.interceptors.push('authInterceptor')
    });
