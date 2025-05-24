from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["https://client-production-ccf0.up.railway.app"])
    from .routes import register_routes
    register_routes(app)

    from .sockets.events import register_socket_events
    register_socket_events(socketio)

    socketio.init_app(app)
    return app
