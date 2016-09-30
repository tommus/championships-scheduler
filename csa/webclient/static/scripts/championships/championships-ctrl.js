'use strict';

angular.module('csa')
.controller('ChampionshipsCtrl', function($scope, $q, Championships) {

    $scope.championships = [];

    $q.all([Championships.query()])
        .spread(function(championships) {
            $scope.championships = championships.data;
        });
});
