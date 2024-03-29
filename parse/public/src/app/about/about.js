angular.module( 'ngBoilerplate.about', [
  'ui.router',
  'placeholders',
  'ui.bootstrap'
])

.config(function config( $stateProvider ) {
  $stateProvider.state( 'about', {
    url: '/about',
    views: {
      "main": {
        controller: 'AboutCtrl',
        templateUrl: 'about/about.tpl.html'
      }
    },
    data:{ pageTitle: 'Labeling Data' }
  });
})

.controller( 'AboutCtrl', function AboutCtrl( $scope, $sce ) {
  $scope.currentUrl = "";
  $scope.currentUrlString = "";
  $scope.labels = {"yellowLabel": "yellow", "politicalLabel": "conservative", "positionLabel": "critical"}

  $scope.isLoadingLinks = false;
  $scope.noNewLinks = false;

  $scope.getStats = function() {
    var Link = Parse.Object.extend("Link");
    var query = new Parse.Query(Link);
    query.limit(202);
    query.find({
      success: function(links) {
        var yellowLabelStats = {"yellow": 0, "nonyellow": 0}, politicalLabelStats = {"conservative": 0, "liberal": 0, "neutral": 0}, positionLabelStats = {"critical": 0, "defensive": 0, "factual": 0};

        links.forEach(function(link) {
          yellowLabelStats[link.get("yellowLabels")[0]]++;
          politicalLabelStats[link.get("politicalLabels")[0]]++;
          positionLabelStats[link.get("positionLabels")[0]]++;
        })

        console.log(yellowLabelStats);
        console.log(politicalLabelStats);
        console.log(positionLabelStats);
      },
      error: function(error) {
        console.log("links error");
        console.log(error);
      }
    })
  }

  $scope.getStats();

  $scope.fetchUrlLink = function() {
    if($scope.isLoadingLinks)
      return;

    $scope.isLoadingLinks = true;

    Parse.Cloud.run("getLinkToLabel", {}).then(function(obj) {
      $scope.isLoadingLinks = false;

      if(obj.url) {
        $scope.currentUrl = $sce.trustAsResourceUrl(obj.url);
        $scope.currentUrlString = obj.url;
        $scope.noNewLinks = false;
      } else {
        $scope.noNewLinks = true;
      }
    }, function(error) {
      console.log(error);
      $scope.isLoadingLinks = false;
      if(error.message)
        alert(error.message + " Please try again or check the console for the error.");
      else
        alert("An error occured. Please try again or check the console for the error.");
      return;
    });
  }

  $scope.fetchUrlLink();

  $scope.addLabels = function() {
    if($scope.labels.yellowLabel == "" || $scope.labels.politicalLabel == "" || $scope.labels.positionLabel == "") {
      alert("Choose a label for each one.");
      return;
    }

    var params = {"url": $scope.currentUrlString, "yellowLabel": $scope.labels.yellowLabel, "politicalLabel": $scope.labels.politicalLabel, "positionLabel": $scope.labels.positionLabel}

    Parse.Cloud.run("addLabel", params).then(function() {
      alert("Labeled successfully.");
      $scope.labels = {"yellowLabel": "yellow", "politicalLabel": "conservative", "positionLabel": "critical"}

      $scope.fetchUrlLink();
    }, function(error) {
      console.log(error);
      if(error.message)
        alert(error.message + " Please try again or check the console for the error.");
      else
        alert("An error occured. Please try again or check the console for the error.");
      return;
    });
  }
})

;
