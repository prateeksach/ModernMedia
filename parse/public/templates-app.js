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
    "        <input id=\"topicInput\" type=\"text\" class=\"form-control\" placeholder=\"ISIS, Crimea, etc.\" ng-model=\"addObj.topic\" />\n" +
    "      </div>\n" +
    "\n" +
    "      <div class=\"form-group\">\n" +
    "        <label for=\"orgInput\">Article Organization</label>\n" +
    "        <input id=\"orgInput\" type=\"text\" class=\"form-control\" placeholder=\"Fox, CNN, etc.\" ng-model=\"addObj.org\" />\n" +
    "      </div>\n" +
    "\n" +
    "      <button type=\"submit\" class=\"btn btn-default\" ng-click=\"addLink()\">Add</button>\n" +
    "    </form>\n" +
    "  </div>\n" +
    "</div>\n" +
    "");
}]);
