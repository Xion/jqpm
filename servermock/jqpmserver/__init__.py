"""
jQuery Package Manager -- Mock server
Main file
"""
import sys
import json
import os

from flask import Flask, abort, make_response

from jqpmserver import github


app = Flask(__name__)


@app.route('/<name:str>', methods=['GET'])
def plugin(name):
    """Request handler to retrieve information of given plugin.

    Returned JSON contains the jquery.json manifest under "manifest" key
    and the URL to download actual plugin JS file under "url" key.

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
    plugin_url, plugin_name = None
    for fname, url in files.iteritems():
        fname = fname.lower()
        basename, ext = os.path.splitext(fname)
        if ext != 'js':
            continue
        if basename.startswith('jquery.'):
            plugin_name = basename[len('jquery.'):]
            plugin_url = url
            break
    else:
        abort(404)

    # create manifest
    manifest = {
        "name": plugin_name,
        "title": repo['name'],
        "author": {
            "name": repo['owner'],
            "url": "http://github.com/%s" % repo['owner'],
        },
        "homepage": "http://github.com/%s/%s" % (repo['owner'], repo['name'])
    }

    return make_response(json.dumps({'manifest': manifest, 'url': plugin_url}),
                         mimetype='application/json')


# Running the server

def main():
    """Run the server."""
    port = 5000 if len(sys.argv) < 1 else int(sys.argv[0])
    app.run(port=port)
