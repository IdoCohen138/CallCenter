# run.py

import os
from app import create_app, socketio

flask_app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(flask_app, host="0.0.0.0", port=port, debug=False)
