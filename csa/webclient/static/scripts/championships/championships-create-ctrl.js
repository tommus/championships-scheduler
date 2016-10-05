'use strict';

angular.module('csa')
    .controller('ChampionshipsCreateCtrl', function($scope, $location, Championships, Participates, Accounts, Teams) {

        $scope.groups = [ 1, 2, 3, 4, 5, 6, 7, 8 ];
        $scope.players_teams_per_group = [ 1, 2, 3, 4, 5, 6, 7, 8 ];
        $scope.home_away = [{ 'id': 1, 'text': 'Single game only'}, { 'id': 2, 'text': 'Home and away' } ];

        $scope.request = {
            'name': '',
            'groups': 1,
            'player_teams_per_group': 1,
            'participates': [],
            'home_away': true
        };

        $scope.originalRequest = angular.copy($scope.request);

        function getUser(id) {
            if($scope.accounts === undefined) {
                return;
            }

            var users = $scope.accounts.filter(function(account) {
                return account.id == id;
            });

            return users[0];
        }

        function getTeam(id) {
            if($scope.teams === undefined) {
                return;
            }

            var teams = $scope.teams.filter(function(team) {
                return team.id == id;
            });

            return teams[0];
        }

        $scope.getParticipate = function(participate) {
            var team = getTeam(participate.team);
            var user = getUser(participate.player);
            return {
                'participate': participate,
                'team': team,
                'user': user
            }
        };

        $scope.resetValues = function() {
            $scope.request = $scope.originalRequest;
        };

        $scope.submitValues = function() {
            // TODO: To be implemented.
        };

        Participates.query().then(function(participates) {
           $scope.participates = participates.data;
        });

        Accounts.query().then(function(accounts) {
            $scope.accounts = accounts.data;
        });

        Teams.query().then(function(teams) {
            $scope.teams = teams.data;
        });
    });
