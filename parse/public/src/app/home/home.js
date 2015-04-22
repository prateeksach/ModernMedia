/**
 * Each section of the site has its own module. It probably also has
 * submodules, though this boilerplate is too simple to demonstrate it. Within
 * `src/app/home`, however, could exist several additional folders representing
 * additional modules that would then be listed as dependencies of this one.
 * For example, a `note` section could have the submodules `note.create`,
 * `note.delete`, `note.edit`, etc.
 *
 * Regardless, so long as dependencies are managed correctly, the build process
 * will automatically take take of the rest.
 *
 * The dependencies block here is also where component dependencies should be
 * specified, as shown below.
 */
angular.module( 'ngBoilerplate.home', [
  'ui.router',
  'parse-angular'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider ) {
  $stateProvider.state( 'home', {
    url: '/home',
    views: {
      "main": {
        controller: 'HomeCtrl',
        templateUrl: 'home/home.tpl.html'
      }
    },
    data:{ pageTitle: 'Add Link' }
  });
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'HomeCtrl', function HomeController( $scope ) {
  $scope.addObj = {"url": "", "topic": "", "org": "", "yellowLabel": "", "politicalLabel": "", "biasLabel": "Biased", "opinionLabel": ""};
  $scope.isAddingLink = false;

  $scope.addLink = function() {
    if($scope.isAddingLink)
      return;

    if(!$scope.addObj.url || !$scope.addObj.topic || !$scope.addObj.org || !$scope.addObj.yellowLabel || !$scope.addObj.politicalLabel || !$scope.addObj.biasLabel || !$scope.addObj.opinionLabel) {
      alert("Please enter all fields.");
      return;
    }

    $scope.isAddingLink = true;

    Parse.Cloud.run("addLink", $scope.addObj).then(function() {
      alert("Added successfully.");

      $scope.addObj.url = ""
      $scope.isAddingLink = false;
    }, function(error) {
      $scope.isAddingLink = false;

      console.log(error);
      if(error.message)
        alert(error.message + " Please try again or check the console for the error.");
      else
        alert("An error occured. Please try again or check the console for the error.");
    });
  }
})

;

