from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from werkzeug.middleware.proxy_fix import ProxyFix


socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)


    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


    CORS(app, origins="*")

    from .routes import register_routes
    register_routes(app)

    from .sockets.events import register_socket_events
    register_socket_events(socketio)
    socketio.init_app(
        app,
        cors_allowed_origins="*",
        logger=True,
        engineio_logger=True
    )

    return app
