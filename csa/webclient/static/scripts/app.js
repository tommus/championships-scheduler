"use strict";

angular.module("csa", ["ngRoute", "ngSanitize", "$q-spread", "settings"])
    .config(function ($routeProvider, $httpProvider, settings) {
        $routeProvider
            .when("/", {
                templateUrl: settings.STATIC_URL + "partials/championships.html",
                controller:  "ChampionshipsCtrl"
            })
            .otherwise({
                redirectTo: "/"
            });
        $httpProvider.defaults.xsrfCookieName = "csrftoken";
        $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";
    });
