# wsgi.py

import eventlet
eventlet.monkey_patch()  

from app import create_app, socketio

app = create_app()
