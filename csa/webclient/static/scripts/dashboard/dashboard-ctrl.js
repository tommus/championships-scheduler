'use strict';

angular.module('csa')
  .controller('DashboardCtrl', function ($scope, $q, Championships, Groups, Matches) {

    $scope.championshipsCount = 0;
    $scope.groupsCount        = 0;
    $scope.matchesCount       = 0;

    $scope.loadData = function () {
      $q.all([
        Championships.all(),
        Groups.all(),
        Matches.all()
      ]).then(function (data) {
        $scope.championshipsCount = data[0].data.length;
        $scope.groupsCount        = data[1].data.length;
        $scope.matchesCount       = data[2].data.length;
      });
    };
    $scope.loadData();
  });
