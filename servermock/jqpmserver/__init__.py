"""
jQuery Package Manager -- Mock server
Main file
"""
import sys

from flask import Flask
import requests


app = Flask(__name__)





def main():
    """Run the server."""
    port = 5000 if len(sys.argv) < 1 else int(sys.argv[0])
    app.run(port=port)
