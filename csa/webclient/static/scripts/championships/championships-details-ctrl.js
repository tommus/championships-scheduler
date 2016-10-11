'use strict';

angular.module('csa')
  .controller('ChampionshipsDetailsCtrl', function ($scope, $location, $q, $routeParams, Championships, Groups, Results) {

    $scope.loadData = function () {
      $q.all([
        Championships.get($routeParams.id),
        Groups.query({championship: $routeParams.id}),
        Results.query({championship: $routeParams.id})
      ]).then(function (data) {
        $scope.championships = data[0].data;
        $scope.groups        = data[1].data;
        $scope.results       = data[2].data;

        sortGroupParticipatesByResults($scope.groups, $scope.results);
      });
    };
    $scope.loadData();

    $scope.getById = getById;
  });

function getById(collection, id) {
  var result = collection.filter(function (item) {
    return item.id === id
  });
  return result[0];
}

function sortGroupParticipatesByResults(groups, results) {
  groups.forEach(function (group) {
    group.participates = sortByResults(group.participates, results)
  });
}

function sortByResults(participates, results) {
  return participates.sort(function (a, b) {
    var aResults = getById(results, a).results;
    var bResults = getById(results, b).results;
    if (aResults['points'] === bResults['points']) {
      if (aResults['goals_balance'] === bResults['goals_balance']) {
        return aResults['games_played'] === bResults['games_played'];
      }
      return aResults['goals_balance'] < bResults['goals_balance'];
    }
    return aResults['points'] < bResults['points'];
  });
}
