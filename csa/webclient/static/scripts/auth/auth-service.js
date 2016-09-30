'use strict';

angular.module('csa')
    .service('Auth', function ($http, $interval, $cookieStore, $localStorage, settings) {
        var intervals = [];
        return {
            login:              function (credentials) {
                return $http.post(settings.BASE_URL + '/login/', credentials);
            },
            logout:             function () {
                $cookieStore.remove(settings.USER_LOGIN_ID_COOKIE);
                return $http.post(settings.BASE_URL + '/logout/');
            },
            setCurrentUser:     function (user, remember) {
                if (user === null || user === undefined) {
                    $cookieStore.remove(settings.USER_LOGIN_ID_COOKIE);
                    if (!remember)
                        $localStorage.user = null;
                }
                else {
                    $cookieStore.put(settings.USER_LOGIN_ID_COOKIE, user.username);
                    if (remember)
                        $localStorage.user = user.username
                }
            },
            getCurrentUser:     function () {
                return $localStorage.user || $cookieStore.get(settings.USER_LOGIN_ID_COOKIE)
            },
            addInterval:        function (interval) {
                intervals.push(interval)
            },
            cancelAllIntervals: function (interval) {
                while (intervals.length) {
                    $interval.cancel(intervals.pop());
                }
            }
        }
    });