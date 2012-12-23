from flask import Flask

app = Flask(__name__)

if not app.debug:
    import logging, sys
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.WARNING)
    app.logger.addHandler(handler)
