from flask import Flask
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

if not app.debug:
    import logging, sys
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.WARNING)
    app.logger.addHandler(handler)
