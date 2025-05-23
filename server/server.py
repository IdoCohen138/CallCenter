from flask import Flask, request, jsonify
from flask_cors import CORS
from db.database import (
    get_all_tags, add_tag,
    create_call, get_all_calls, assign_tag_to_call,
    create_task, assign_task_to_call, update_task_status, get_tasks_for_call
)

app = Flask(__name__)
CORS(app)

# --- TAGS ---
@app.route('/api/tags', methods=['GET'])
def fetch_tags():
    return jsonify(get_all_tags())

@app.route('/api/tags', methods=['POST'])
def create_tag():
    data = request.get_json()
    add_tag(data['name'])
    return jsonify({'status': 'Tag created'}), 201

# --- CALLS ---
@app.route('/api/calls', methods=['POST'])
def create_call_route():
    data = request.get_json()
    call_id = create_call(data['description'])
    return jsonify({'id': call_id}), 201

@app.route('/api/calls', methods=['GET'])
def get_calls():
    return jsonify(get_all_calls())

@app.route('/api/calls/<int:call_id>/tags', methods=['POST'])
def assign_tag(call_id):
    data = request.get_json()
    tag_id = data['tag_id']
    assign_tag_to_call(call_id, tag_id)
    return jsonify({'status': 'Tag assigned'}), 200

# --- TASKS ---
@app.route('/api/tasks', methods=['POST'])
def create_task_route():
    data = request.get_json()
    task_id = create_task(data['name'])
    return jsonify({'id': task_id}), 201

@app.route('/api/calls/<int:call_id>/tasks', methods=['POST'])
def assign_task(call_id):
    data = request.get_json()
    task_id = data['task_id']
    assign_task_to_call(call_id, task_id)
    return jsonify({'status': 'Task assigned'}), 200

@app.route('/api/tasks/<int:task_id>/status', methods=['PUT'])
def update_status(task_id):
    data = request.get_json()
    status = data['status']
    update_task_status(task_id, status)
    return jsonify({'status': 'Task updated'}), 200

@app.route('/api/calls/<int:call_id>/tasks', methods=['GET'])
def get_call_tasks(call_id):
    return jsonify(get_tasks_for_call(call_id))
    
# --- USERS ---
@app.route('/api/users', methods=['GET'])
def fetch_users():
    from db.database import get_all_users
    return jsonify(get_all_users())

@app.route('/api/login', methods=['POST'])
def login():
    from db.database import get_user_by_username
    data = request.get_json()
    username = data.get('username')
    user = get_user_by_username(username)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
