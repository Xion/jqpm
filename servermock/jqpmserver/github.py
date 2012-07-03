"""
GitHub API calls.
"""
import json
from urllib import quote, urlencode
from base64 import b64decode
from StringIO import StringIO

import requests


GITHUB_URL = "https://api.github.com"


def search_repos(query):
    """Search GitHub for repositories matching given query.
    Returns a list of dicts.
    """
    url = "%s/legacy/repos/search/%s" % (GITHUB_URL, quote(query))
    response = requests.get(url)

    repos = json.loads(response.content)
    return repos['repositories']


def list_files(user, repo, ref='master'):
    """Lists all files in root directory of ``repo`` belonging
    to given ``user``.
    Returns a dictionary mapping file and directory names to URLs.
    """
    url = "%s/repos/%s/%s/git/trees/%s" % (GITHUB_URL, user, repo, ref)
    response = requests.get(url)

    tree_info = json.loads(response.content)
    return dict(
        ("%s%s" % (t['path'], "/" if t['type'] == 'tree' else ''), t['url'])
        for t in tree_info['tree']
    )


def get_commits(user, repo, from_ref=None, path=None):
    """Gets list of commits from ``repo`` belonging to given ``user``,
    optionally filtering by ``path`` and/or starting from given ``ref``.
    Returns a list of dictionaries.
    """
    args = {}
    if from_ref is not None:
        args['sha'] = from_ref
    if path is not None:
        args['path'] = path

    url = "%s/repos/%s/%s/commits" % (GITHUB_URL, user, repo)
    if args:
        url += "?%s" % urlencode(args)
    response = requests.get(url)

    return json.loads(response.content)


def retrieve_file(user, repo, path, ref='master'):
    """Retrieves contents of file under ``path`` from a ``repo``
    that belongs to given ``user``.
    Returns a file-like object with file content.
    """
    if path.startswith('/'):
        path = path[1:]

    url = "%s/repos/%s/%s/contents/%s" % (GITHUB_URL, user, repo, path)
    url += "?%s" % urlencode({'ref': ref})
    response = requests.get(url)

    file_info = json.loads(response.content)
    return StringIO(b64decode(file_info['content']))
