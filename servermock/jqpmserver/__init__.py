"""
jQuery Package Manager -- Mock server
Main file
"""
import sys
import json
import os

from flask import Flask, abort, make_response
from dateutil.parser import parse as parse_date

from jqpmserver import github


app = Flask(__name__)


@app.route('/<name>', methods=['GET'])
def plugin(name):
    """Request handler to retrieve information of given plugin.

    Returned JSON contains the jquery.json manifest under "manifest" key,
    the URL to download actual plugin JS file under "url" key
    and the date of last modification under "date" key.

    .. note:: The manifest is generated on the fly
              and contains only minimum information.
              It's just a mock server, after all.
    """
    repos = github.search_repos(name)
    if not repos:
        abort(404)
    repo = repos[0]

    # find something that looks like plugin's JS file
    files = github.list_files(repo['owner'], repo['name'])
    plugin = {}
    for fname, url in files.iteritems():
        basename, ext = os.path.splitext(fname.lower())
        if ext != 'js':
            continue
        if basename.startswith('jquery.'):
            plugin = {
                'name': basename[len('jquery.'):],
                'filename': fname,
                'url': url,
            }
            break
    else:
        abort(404)

    # create manifest
    manifest = {
        "name": plugin['name'],
        "title": repo['name'],
        "author": {
            "name": repo['owner'],
            "url": "http://github.com/%s" % repo['owner'],
        },
        "homepage": "http://github.com/%s/%s" % (repo['owner'], repo['name'])
    }

    # use date of last commit that changed the plugin file
    commits = github.get_commits(repo['owner'], repo['name'],
                                 path=plugin['filename'])
    date = max(commits,
               key=lambda c: parse_date(c['commit']['commiter']['date']))

    response = {
        'manifest': manifest,
        'url': plugin['url'],
        'date': date,
    }
    return make_response(json.dumps(response), mimetype='application/json')


# Running the server

def main():
    """Run the server."""
    port = 5000 if len(sys.argv) <= 1 else int(sys.argv[1])
    app.run(port=port)
