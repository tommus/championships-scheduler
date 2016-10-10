'use strict';

angular.module('csa')
    .controller('ChampionshipsCreateCtrl', function($scope, $location, Championships, Participates, Accounts, Teams) {

        $scope.groups = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ];
        $scope.home_away = [{ 'id': 1, 'text': 'Single game only'}, { 'id': 2, 'text': 'Home and away' } ];
        $scope.players = [];
        $scope.teams = [];

        $scope.request = {
            'name': '',
            'groups': 1,
            'players': [],
            'teams': [],
            'home_away': true
        };

        $scope.originalRequest = angular.copy($scope.request);

        $scope.resetValues = function() {
            $scope.request = $scope.originalRequest;
        };

        $scope.submitValues = function() {
            // TODO: To be implemented.
            Championships.schedule($scope.request).then(function(response) {
                console.log(response);
            });
        };

        Participates.query().then(function(participates) {
           $scope.participates = participates.data;
        });

        Accounts.query().then(function(accounts) {
            $scope.players = accounts.data;
        });

        Teams.query().then(function(teams) {
            $scope.teams = teams.data;
        });
    });
