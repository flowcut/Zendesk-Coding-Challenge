"""ZTicketViewer development configuration."""

import pathlib
from requests.auth import HTTPBasicAuth

APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = \
    b'*\xca\xc7\x1a\x82\x1fY\xb0\xea"m\xb5m\x8a\n\xe2\xefp\xc9p\x0b3{\xa4'
SESSION_COOKIE_NAME = 'login'

TICKETS_FETCH_COUNT = 100
TICKETS_DISPLAY_COUNT = 25

TEST_AUTH = HTTPBasicAuth(username="umink@umich.edu", password="Awin1m2n3b")

ZTICKETVIEWER_ROOT = pathlib.Path(__file__).resolve().parent.parent
