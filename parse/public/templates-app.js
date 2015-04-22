angular.module('templates-app', ['about/about.tpl.html', 'home/home.tpl.html']);

angular.module("about/about.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("about/about.tpl.html",
    "<div class=\"label-page\">\n" +
    "  <div class=\"row\">\n" +
    "    <div class=\"col-md-12\">\n" +
    "      <h1>Labeling</h1>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "\n" +
    "  <div class=\"row\" ng-if=\"currentUrlString.length == 0\">\n" +
    "    <p ng-if=\"isLoadingLinks\">Loading new links...</p>\n" +
    "    <p ng-if=\"!isLoadingLinks && noNewLinks\">No new links in the database</p>\n" +
    "  </div>\n" +
    "  <div class=\"row\" ng-if=\"currentUrlString.length\">\n" +
    "    <div class=\"col-md-9\">\n" +
    "      <div class=\"iframe-holder\">\n" +
    "        <iframe ng-src=\"{{currentUrl}}\"></iframe>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "    <div class=\"col-md-3\">\n" +
    "      <div class=\"select-container\">\n" +
    "        <select ng-model=\"labels.yellowLabel\">\n" +
    "          <option value=\"yellow\">Yellow</option>\n" +
    "          <option value=\"nonyellow\">Non-Yellow</option>\n" +
    "        </select>\n" +
    "      </div>\n" +
    "\n" +
    "      <div class=\"select-container\">\n" +
    "        <select ng-model=\"labels.politicalLabel\">\n" +
    "          <option value=\"conservative\">Conservative</option>\n" +
    "          <option value=\"liberal\">Liberal</option>\n" +
    "          <option value=\"neutral\">Neutral</option>\n" +
    "        </select>\n" +
    "      </div>\n" +
    "\n" +
    "      <div class=\"select-container\">\n" +
    "        <select ng-model=\"labels.positionLabel\">\n" +
    "          <option value=\"critical\">Critical</option>\n" +
    "          <option value=\"defensive\">Defensive</option>\n" +
    "          <option value=\"factual\">Strictly Factual</option>\n" +
    "        </select>\n" +
    "      </div>\n" +
    "\n" +
    "      <button type=\"submit\" class=\"btn btn-default\" ng-click=\"addLabels()\">Add Label</button>\n" +
    "  </div>\n" +
    "</div>");
}]);

angular.module("home/home.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("home/home.tpl.html",
    "<div class=\"row\">\n" +
    "  <div class=\"col-md-12\">\n" +
    "    <h1>Add a Link</h1>\n" +
    "    <p>\n" +
    "    BEWARE: Please remove get variables at the end of URLs (anything with ? or & should be removed) but obviously, make sure the URL still works before you submit.\n" +
    "    </p>\n" +
    "  </div>\n" +
    "</div>\n" +
    "<div class=\"row\">\n" +
    "  <div class=\"col-md-6\">\n" +
    "    <form>\n" +
    "      <div class=\"form-group\">\n" +
    "        <label for=\"urlInput\">Link URL</label>\n" +
    "        <input id=\"urlInput\" type=\"text\" class=\"form-control\" placeholder=\"http://example.com\" ng-model=\"addObj.url\" />\n" +
    "      </div>\n" +
    "\n" +
    "      <div class=\"form-group\">\n" +
    "        <label for=\"topicInput\">Article Topic</label>\n" +
    "        <select class=\"form-control\" ng-model=\"addObj.topic\">\n" +
    "          <option value=\"Marijuana Legalization\">Marijuana Legalization</option>\n" +
    "          <option value=\"Abortion\">Abortion</option>\n" +
    "          <option value=\"Gay Marriage\">Gay Marriage</option>\n" +
    "          <option value=\"NSA Spying\">NSA Spying</option>\n" +
    "          <option value=\"Obamacare\">Obamacare</option>\n" +
    "          <option value=\"Climate Change\">Climate Change</option>\n" +
    "          <option value=\"Immigration\">Immigration</option>\n" +
    "          <option value=\"Gun Control\">Gun Control</option>\n" +
    "        </select>\n" +
    "      </div>\n" +
    "\n" +
    "      <div class=\"form-group\">\n" +
    "        <label for=\"orgInput\">Article Organization</label>\n" +
    "        <select class=\"form-control\" ng-model=\"addObj.org\">\n" +
    "          <option value=\"USA Today\">USA Today</option>\n" +
    "          <option value=\"New York Post\">New York Post</option>\n" +
    "          <option value=\"CNN\">CNN</option>\n" +
    "          <option value=\"FOX\">FOX</option>\n" +
    "          <option value=\"ThinkProgress\">ThinkProgress</option>\n" +
    "          <option value=\"Huffington Post\">Huffington Post</option>\n" +
    "          <option value=\"New Republic\">New Republic</option>\n" +
    "          <option value=\"New York Times\">New York Times</option>\n" +
    "        </select>\n" +
    "      </div>\n" +
    "\n" +
    "      <div class=\"form-group\">\n" +
    "        <label for=\"topicInput\">Yellowism Label:&nbsp;&nbsp;&nbsp;</label>\n" +
    "        <label class=\"radio-inline\">\n" +
    "          <input type=\"radio\" name=\"yellowLabel\" value=\"Yellow\" ng-model=\"addObj.yellowLabel\"> Yellow\n" +
    "        </label>\n" +
    "        <label class=\"radio-inline\">\n" +
    "          <input type=\"radio\" name=\"yellowLabel\" value=\"Not Yellow\" ng-model=\"addObj.yellowLabel\"> Not Yellow\n" +
    "        </label>\n" +
    "      </div>\n" +
    "\n" +
    "      <div class=\"form-group\">\n" +
    "        <label for=\"topicInput\">Political Label:&nbsp;&nbsp;&nbsp;</label>\n" +
    "        <label class=\"radio-inline\">\n" +
    "          <input type=\"radio\" name=\"politicalLabel\" value=\"Conservative\" ng-model=\"addObj.politicalLabel\"> Conservative\n" +
    "        </label>\n" +
    "        <label class=\"radio-inline\">\n" +
    "          <input type=\"radio\" name=\"politicalLabel\" value=\"Liberal\" ng-model=\"addObj.politicalLabel\"> Liberal\n" +
    "        </label>\n" +
    "        <label class=\"radio-inline\">\n" +
    "          <input type=\"radio\" name=\"politicalLabel\" value=\"Neutral\" ng-model=\"addObj.politicalLabel\"> Neutral\n" +
    "        </label>\n" +
    "      </div>\n" +
    "\n" +
    "      <div class=\"form-group hide\">\n" +
    "        <label for=\"topicInput\">Bias Label:&nbsp;&nbsp;&nbsp;</label>\n" +
    "        <label class=\"radio-inline\">\n" +
    "          <input type=\"radio\" name=\"biasLabel\" value=\"Biased\" ng-model=\"addObj.biasLabel\"> Biased\n" +
    "        </label>\n" +
    "        <label class=\"radio-inline\">\n" +
    "          <input type=\"radio\" name=\"biasLabel\" value=\"Not Biased\" ng-model=\"addObj.biasLabel\"> Not Biased\n" +
    "        </label>\n" +
    "      </div>\n" +
    "\n" +
    "      <div class=\"form-group\">\n" +
    "        <label for=\"topicInput\">Opinion Label:&nbsp;&nbsp;&nbsp;</label>\n" +
    "        <label class=\"radio-inline\">\n" +
    "          <input type=\"radio\" name=\"opinionLabel\" value=\"Opinion Article\" ng-model=\"addObj.opinionLabel\"> Opinion Article\n" +
    "        </label>\n" +
    "        <label class=\"radio-inline\">\n" +
    "          <input type=\"radio\" name=\"opinionLabel\" value=\"Other\" ng-model=\"addObj.opinionLabel\"> Other\n" +
    "        </label>\n" +
    "      </div>\n" +
    "\n" +
    "      <button type=\"submit\" class=\"btn btn-default\" ng-click=\"addLink()\">\n" +
    "        <span ng-if=\"isAddingLink\">Adding... Please Wait.</span>\n" +
    "        <span ng-if=\"!isAddingLink\">Add Link</span>\n" +
    "      </button>\n" +
    "    </form>\n" +
    "  </div>\n" +
    "</div>\n" +
    "");
}]);
