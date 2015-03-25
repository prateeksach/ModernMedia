// Require modules
var _ = require('underscore');

// Parse Objects
var Link = Parse.Object.extend("Link");
var Label = Parse.Object.extend("Label");

// Add new link to database
Parse.Cloud.define("addLink", function(request, response) {
  	if(!request.params.url || !request.params.topic || !request.params.org) {
		response.error("Error: Invalid parameters.");
		return;
	}

	var query = new Parse.Query(Link);
	query.equalTo("url", request.params.url);

	query.first({
		useMasterKey: true,
		success: function(item) {
			if(item) {
				response.error("Link already exists.");
			} else {
				var link = new Link();
				link.set("url", request.params.url);
				link.set("topic", request.params.topic);
				link.set("organization", request.params.org);
				link.set("dataScrapped", false);

				link.save(null, {
					useMasterKey: true,
					success: function(success) {
						response.success();
					}, 
					error: function(error) {
						response.error(error);
					}
				})
			}
		},
		error: function(error) {
			response.error(error);
		}
	})
});

// Get a list of all unscrapped links
Parse.Cloud.define("addLink", function(request, response) {
	var query = new Parse.Query(Link);
	query.equalTo("dataScrapped", false);

	query.find({
		useMasterKey: true,
		success: function(list) {
			response.success(list);
		},
		error: function(error) {
			response.error(error);
		}
	})
});

// Mark a link as scrapped
Parse.Cloud.define("markAsScrapped", function(request, response) {
  	if(!request.params.url) {
		response.error("Error: Invalid parameters.");
		return;
	}

	var query = new Parse.Query(Link);
	query.equalTo("url", request.params.url);

	query.first({
		useMasterKey: true,
		success: function(item) {
			if(item) {
				item.set("dataScrapped", true);
				item.save(null, {
					useMasterKey: true,
					success: function() {
						response.success();
					},
					error: function(error) {
						response.error(error);
					}
				})
			} else {
				response.error("Link does not exist.");
			}
		},
		error: function(error) {
			response.error(error);
		}
	})
});
