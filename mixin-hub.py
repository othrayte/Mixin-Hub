import os

if not app.debug:
    import logging, sys
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.WARNING)
    app.logger.addHandler(handler)

import web

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)