from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

ALLOWED_ORIGINS = [
    "https://client-production-ccf0.up.railway.app",
    "http://localhost:5173"
]

def create_app():
    app = Flask(__name__)
    CORS(app, origins=ALLOWED_ORIGINS)
    socketio = SocketIO(app, cors_allowed_origins=ALLOWED_ORIGINS)
    from .routes import register_routes
    register_routes(app)
    from .sockets.events import register_socket_events
    register_socket_events(socketio)
    return app
