'use strict';

angular.module('csa')
  .controller('ChampionshipsCtrl', function ($scope, $location, $q, Championships) {

    $scope.championships = [];

    $scope.goCreate = function () {
      $location.path('/championships/create');
    };

    Championships.query().then(function (championships) {
      $scope.championships = championships.data;
    });
  });
