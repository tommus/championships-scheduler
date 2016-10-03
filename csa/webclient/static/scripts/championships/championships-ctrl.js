'use strict';

angular.module('csa')
.controller('ChampionshipsCtrl', function($scope, $location, Championships) {

    $scope.championships = [
        {
            'name': 'Master League October 2016',
            'participants': 3,
            'started': 'October 6, 2016',
            'completed': true
        },
        {
            'name': 'Master League November 2016',
            'participants': 4,
            'started': 'November 9, 2016',
            'completed': false
        }
    ];

    $scope.goCreate = function() {
        $location.path('/championships/create');
    };
});
