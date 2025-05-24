from flask import Blueprint, request, jsonify
from app.services.database import create_task, update_task_status, get_all_tasks, link_task_to_tag, rename_task, get_all_task_tag_links
from app import socketio

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['GET'])
def fetch_tasks():
    return jsonify(get_all_tasks())

@tasks_bp.route('', methods=['POST'])
def create_task_route():
    data = request.get_json()
    task_id = create_task(data['name'])
    socketio.emit('tasks_updated', {'action': 'created', 'task_id': task_id})
    return jsonify({'id': task_id}), 201

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def rename_task_route(task_id):
    data = request.get_json()
    rename_task(task_id, data['name'])
    socketio.emit('tasks_updated', {'action': 'renamed', 'task_id': task_id})
    return jsonify({'status': 'Task renamed'}), 200

@tasks_bp.route('/<int:task_id>/status', methods=['PUT'])
def update_status(task_id):
    data = request.get_json()
    update_task_status(task_id, data['status'])
    return jsonify({'status': 'Task updated'}), 200

@tasks_bp.route('/<int:task_id>/tags', methods=['POST'])
def assign_task_to_tag(task_id):
    data = request.get_json()
    link_task_to_tag(task_id, data['tag_id'])
    socketio.emit('link_task_tag', {'action': 'link_task_tag'})
    return jsonify({'status': 'Task linked to tag'}), 200

@tasks_bp.route('/links', methods=['GET'])
def get_all_task_tag_links_route():
    return jsonify(get_all_task_tag_links())
