import os
print("📍 Starting run.py...")

import eventlet
eventlet.monkey_patch()
print("📍 Eventlet monkey patched")

from app import create_app, socketio
print("📍 App and socketio imported")

app = create_app()
print("📍 App created")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"PORT from ENV: {os.environ.get('PORT')}")
    print(f"📍 Starting server on port {port}...")
    socketio.run(app, host='0.0.0.0', port=port)
