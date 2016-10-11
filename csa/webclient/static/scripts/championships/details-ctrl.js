'use strict';

angular.module('csa')
  .controller('ChampionshipsDetailsCtrl', function ($scope, $location, $q, $routeParams, $uibModal, $route, settings, Championships, Groups, Results, Matches, Participates, Teams, Accounts) {

    $scope.loadData = function () {
      $q.all([
        Championships.get($routeParams.id),
        Groups.query({championship: $routeParams.id}),
        Results.query({championship: $routeParams.id}),
        Matches.query({group__championship: $routeParams.id}),
        Participates.query({championship: $routeParams.id}),
        Teams.query({championship: $routeParams.id}),
        Accounts.query({championship: $routeParams.id})
      ]).then(function (data) {
        $scope.championships = data[0].data;
        $scope.groups = data[1].data;
        $scope.results = data[2].data;
        $scope.matches = data[3].data;
        $scope.participates = data[4].data;
        $scope.teams = data[5].data;
        $scope.players = data[6].data;

        sortGroupParticipatesByResults($scope.groups, $scope.results);
      });
    };
    $scope.loadData();

    $scope.getById = getById;
    $scope.getPanelStyle = getPanelStyle;
    $scope.sanitizeScore = sanitizeScore;

    $scope.reset = function () {
      var promises = [];

      $scope.matches.forEach(function (match) {
        promises.push(Matches.patch(match.id, {host_team_goals: null, guest_team_goals: null}))
      });

      $q.all(promises).then(function (response) {
        $route.reload();
      });
    };

    $scope.showSetScore = function (match) {
      $uibModal.open({
        templateUrl: settings.STATIC_URL + '/partials/championships/dialogs/set-score.html',
        animation: true,
        controller: 'SetScoreCtrl',
        resolve: {
          match: function () {
            return match;
          }
        }
      }).closed.then(function () {
        $route.reload();
      });
    }
  });

function getById(collection, id) {
  var result = collection.filter(function (item) {
    return item.id === id
  });
  return result[0];
}

function sortGroupParticipatesByResults(groups, results) {
  groups.forEach(function (group) {
    group.participates = sortByResults(group.participates, results);
  });
}

function sortByResults(participates, results) {
  return participates.sort(function (a, b) {
    var aResults = getById(results, a).results;
    var bResults = getById(results, b).results;

    if (aResults['points'] === bResults['points']) {
      if (aResults['goals_balance'] === bResults['goals_balance']) {
        return bResults['games_played'] - aResults['games_played'];
      }
      return bResults['goals_balance'] - aResults['goals_balance'];
    }
    return bResults.points - aResults.points;
  });
}

function getPanelStyle(match, home) {
  if (match.host_team_goals === null || match.guest_team_goals === null) {
    return 'panel panel-default';
  }
  if (match.host_team_goals > match.guest_team_goals) {
    return home ? 'panel panel-success' : 'panel panel-danger';
  }
  if (match.host_team_goals < match.guest_team_goals) {
    return home ? 'panel panel-danger' : 'panel panel-success';
  }
  return 'panel panel-info';
}

function sanitizeScore(score) {
  if (score === null || score === null) {
    return '-';
  }
  return score;
}