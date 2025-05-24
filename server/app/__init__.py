from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

print("📍 Init socketio")
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    print("📍 Creating app...")
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def home():
        return "Server is alive!"

    print("📍 Registering routes...")
    from .routes import register_routes
    register_routes(app)

    print("📍 Registering socket events...")
    from .sockets.events import register_socket_events
    register_socket_events(socketio)

    print("📍 Initializing socketio with app...")
    socketio.init_app(app)
    return app
