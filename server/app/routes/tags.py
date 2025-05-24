from flask import Blueprint, request, jsonify
from app.services.database import get_all_tags, add_tag, rename_tag, get_tasks_by_tag
from app import socketio

tags_bp = Blueprint('tags', __name__)

@tags_bp.route('', methods=['GET'])
def fetch_tags():
    return jsonify(get_all_tags())

@tags_bp.route('', methods=['POST'])
def create_tag():
    data = request.get_json()
    add_tag(data['name'])
    socketio.emit("tags_updated", {"action": "created"})
    return jsonify({'status': 'Tag created'}), 201

@tags_bp.route('/<int:tag_id>', methods=['PUT'])
def update_tag_name(tag_id):
    data = request.get_json()
    rename_tag(tag_id, data['name'])
    socketio.emit('tags_updated', {'action': 'renamed', 'tag_id': tag_id})
    return jsonify({'status': 'Tag updated'}), 200

@tags_bp.route('/<int:tag_id>/tasks', methods=['GET'])
def get_tasks_by_tag_route(tag_id):
    return jsonify(get_tasks_by_tag(tag_id))
