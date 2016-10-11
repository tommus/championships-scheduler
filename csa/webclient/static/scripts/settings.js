'use strict';

angular.module('settings', [])
  .constant('settings', {
    'BASE_URL':   window.location.origin + '/api',
    'STATIC_URL': 'static/'
  });
