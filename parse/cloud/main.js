// Require modules
var _ = require('underscore');

// Parse Objects
var Link = Parse.Object.extend("Link2");
var Label = Parse.Object.extend("Label");

// Add new link to database
Parse.Cloud.define("addLink", function(request, response) {
  	if(!request.params.url || !request.params.topic || !request.params.org || !request.params.yellowLabel || !request.params.politicalLabel || !request.params.biasLabel || !request.params.opinionLabel) {
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
				link.set("yellowLabel", request.params.yellowLabel);
				link.set("politicalLabel", request.params.politicalLabel);
				link.set("biasLabel", request.params.biasLabel);
				link.set("opinionLabel", request.params.opinionLabel);
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

// Add new label
Parse.Cloud.define("addLabel", function(request, response) {
  	if(!request.params.url || !request.params.yellowLabel || !request.params.politicalLabel || !request.params.positionLabel) {
		response.error("Error: Invalid parameters.");
		return;
	}

	var query = new Parse.Query(Link);
	query.equalTo("url", request.params.url);

	query.first({
		useMasterKey: true,
		success: function(item) {
			if(item) {
				item.set("yellowLabels", item.get("yellowLabels") ? item.get("yellowLabels").push(request.params.yellowLabel) : [request.params.yellowLabel]);
				item.set("politicalLabels", item.get("politicalLabels") ? item.get("politicalLabels").push(request.params.politicalLabel) : [request.params.politicalLabel]);
				item.set("positionLabels", item.get("positionLabels") ? item.get("positionLabels").push(request.params.positionLabel) : [request.params.positionLabel]);

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

// Get a list of links to label
Parse.Cloud.define("getLinksToLabel", function(request, response) {
	var query = new Parse.Query(Link);
	query.equalTo("yellowLabels", null);
	query.equalTo("politicalLabels", null);
	query.equalTo("positionLabels", null);

	query.find({
		useMasterKey: true,
		success: function(list) {
			var result = [];

			list.forEach(function(link) {
				result.push(link.get("url"));
			});

			response.success(result);
		},
		error: function(error) {
			response.error(error);
		}
	})
});

// Get a list of links to label
Parse.Cloud.define("getLinkToLabel", function(request, response) {
	var query = new Parse.Query(Link);
	query.equalTo("yellowLabels", null);
	query.equalTo("politicalLabels", null);
	query.equalTo("positionLabels", null);

	query.first({
		useMasterKey: true,
		success: function(item) {
			if(item)
				response.success({"url": item.get("url")});
			else
				response.success({});
		},
		error: function(error) {
			response.error(error);
		}
	})
});