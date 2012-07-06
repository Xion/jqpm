/**
 * Module for GitHub API calls.
 */

'use strict';


var util = require('util')
  , buffer = require('buffer')
  , querystring = require('querystring')
  , http = require('http')
  , https = require('https')
  , url = require('url')
  ;


var GITHUB_URL = "https://api.github.com";


module.exports = {

	/**
	 * Search for repositories matching given query.
	 * :return: An array of objects with repository infos
	 */
	searchRepos: function(query, callback) {
		var url = util.format("%s/legacy/repos/search/%s",
							  GITHUB_URL, querystring.escape(query));
		httpGet(url, function(err, respBody) {
			if (err) {
				callback(err);
			} else {
				var resp = JSON.parse(respBody);
				callback(null, resp.repositories);
			}
		});
	},

	/**
	 * Lists all files in root directory of ``repo`` belonging
	 * to given ``user``.
	 * :return: Object mapping file and directory names to URLs
	 */
	listFiles: function(user, repo, ref, callback) {
		if (!callback) {
			callback = ref;
			ref = 'master';	// ``ref`` is optional
		}

		var url = util.format("%s/repos/%s/%s/git/trees/%s",
							  GITHUB_URL, user, repo, ref);
		httpGet(url, function(err, respBody) {
			if (err) {
				callback(err);
			} else {
				var resp = JSON.parse(respBody);
				var res = {};
				resp.tree.forEach(function(item) {
					var key = item.path;
					if (item.type === 'tree')
						key += '/';
					res[key] = item.url;
				});
				callback(null, res);
			}
		});
	},

	/**
	 * Gets list of commits from ``repo`` belonging to given ``user``.
	 * :param options: May contain:
	 *                 * ``fromRef`` to specify starting revision
	 *                 * ``path`` includes only commits touching the path
	 * :return: Array of objects with commit infos
	 */
	getCommits: function(user, repo, options, callback) {
		if (!callback) {
			callback = options;
			options = {}; // ``options`` are optional
		}

		var args = {
			sha: (options.fromRef ? options.fromRef : 'master')
		};
		if (options.path)
			args.path = options.path;
		var qsArgs = querystring.encode(args);

		var url = util.format("%s/repos/%s/%s/commits",
							  GITHUB_URL, user, repo);
		if (qsArgs)
			url += "?" + qsArgs;

		httpGet(url, function(err, respBody) {
			if (err) {
				callback(err);
			} else {
				var commits = JSON.parse(respBody);
				callback(null, commits);
			}
		});
	},

	/**
	 * Download file from given URL that points to GitHub file.
	 */
	downloadFile: function(url, callback) {
		httpGet(url, function(err, respBody) {
			if (err) {
				callback(err);
			} else {
				var resp = JSON.parse(respBody);
				var file = base64Decode(resp.content);
				callback(null, file);
			}
		});
	},
};


function httpGet(targetUrl, callback) {
	if (typeof targetUrl === 'string')
		targetUrl = url.parse(targetUrl);
	var protocol = targetUrl.protocol === 'https:' ? https : http;
	var req = protocol.get(targetUrl, function(resp) {
		if (resp.statusCode >= 200 && resp.statusCode < 300) {
			resp.setEncoding('utf8');

			var respBody = "";
			resp.on('data', function(chunk) {
				respBody += chunk;
			});
			resp.on('end', function() {
				callback(null, respBody);
			});
		} else {
			var err = new Error(util.format("HTTP error: %s", resp.statusCode));
			err.statusCode = resp.statusCode;
			callback(err);
		}
	});
	req.on('error', callback);
}

function base64Decode(data) {
	return buffer.Buffer(data, 'base64').toString();
}
