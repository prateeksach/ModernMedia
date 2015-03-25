var PARSE_APP_ID = 'mequ79kBCNp74UrSEcoyty4Jwb3q9frUkuFrSsLE';
var PARSE_JAVASCRIPT_KEY = 'zlETgkn9ufqKl4vQDP65tB6dr6EfMnmEbAN1By9h';

Parse.initialize(PARSE_APP_ID, PARSE_JAVASCRIPT_KEY);

angular.module( 'ngBoilerplate', [
  'templates-app',
  'templates-common',
  'ngBoilerplate.home',
  'ngBoilerplate.about',
  'ui.router'
])

.config( function myAppConfig ( $stateProvider, $urlRouterProvider ) {
  $urlRouterProvider.otherwise( '/home' );
})

.run( function run () {
})

.controller( 'AppCtrl', function AppCtrl ( $scope, $location ) {
  $scope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams){
    if ( angular.isDefined( toState.data.pageTitle ) ) {
      $scope.pageTitle = toState.data.pageTitle + '' ;
    }
  });
})

;

