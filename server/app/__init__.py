from flask import Flask, request, redirect
from flask_cors import CORS
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)

    CORS(app, origins=["https://client-production-ccf0.up.railway.app"])

    @app.before_request
    def enforce_https_in_production():
        if app.env == "production":
            if request.headers.get("X-Forwarded-Proto", "http") != "https":
                url = request.url.replace("http://", "https://", 1)
                return redirect(url, code=301)

    from .routes import register_routes
    register_routes(app)

    from .sockets.events import register_socket_events
    register_socket_events(socketio)

    socketio.init_app(app)
    return app
