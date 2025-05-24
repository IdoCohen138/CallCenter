from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from werkzeug.middleware.proxy_fix import ProxyFix

socketio = SocketIO(cors_allowed_origins=[
    "https://client-production-a326.up.railway.app",
    "https://client-production-ccf0.up.railway.app"
])

def create_app():
    print("📍 Flask app loaded — CORS configured")

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    CORS(
        app,
        origins=[
            "https://client-production-a326.up.railway.app",
            "https://client-production-ccf0.up.railway.app"
        ],
        supports_credentials=True,
        resources={
            r"/api/*": {
                "origins": [
                    "https://client-production-a326.up.railway.app",
                    "https://client-production-ccf0.up.railway.app"
                ]
            }
        }
    )

    from .routes import register_routes
    register_routes(app)

    from .sockets.events import register_socket_events
    register_socket_events(socketio)

    socketio.init_app(
        app,
        cors_allowed_origins=[
            "https://client-production-a326.up.railway.app",
            "https://client-production-ccf0.up.railway.app"
        ],
        logger=True,
        engineio_logger=True
    )

    return app
