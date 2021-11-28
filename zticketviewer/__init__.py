"""ZTicketViewer package initializer."""
import flask

app = flask.Flask(__name__)  # pylint: disable=invalid-name

app.config.from_object('zticketviewer.config')

app.config.from_envvar('ZTICKETVIEWER_SETTINGS', silent=True)

import zticketviewer.views  # noqa: E402  pylint: disable=wrong-import-position
