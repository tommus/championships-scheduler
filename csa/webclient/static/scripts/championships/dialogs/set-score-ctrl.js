'use strict';

angular.module('csa')
  .controller('SetScoreCtrl', function ($scope, $uibModalInstance, $q, Participates, Teams, Matches, Accounts, match) {

    $scope.match = match;

    $scope.loadData = function () {
      $q.all([
        Participates.get(match.host_team),
        Participates.get(match.guest_team)
      ]).then(function (data) {
        var hostParticipate = data[0].data;
        var guestParticipate = data[1].data;

        $q.all([
          Teams.get(hostParticipate.team),
          Teams.get(guestParticipate.team),
          Accounts.get(hostParticipate.player),
          Accounts.get(guestParticipate.player)
        ]).then(function (data) {
          $scope.hostTeam = data[0].data;
          $scope.guestTeam = data[1].data;
          $scope.hostPlayer = data[2].data;
          $scope.guestPlayer = data[3].data;
        });
      });
    };
    $scope.loadData();

    $scope.submit = function() {
        Matches.patch(match.id, {
          host_team_goals: match.host_team_goals,
          guest_team_goals: match.guest_team_goals
        }).then(function(response) {
            console.log(response);
            $uibModalInstance.dismiss();
        }).then(function(error) {
          console.log(error);
        });
    };

    $scope.cancel = function() {
      $uibModalInstance.dismiss();
    }
  });
