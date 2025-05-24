from flask import Blueprint, request, jsonify
from app.services.database import create_call, get_all_calls, assign_tag_to_call, get_tags_for_call_db, assign_task_to_call, get_tasks_for_call

calls_bp = Blueprint('calls', __name__)

@calls_bp.route('', methods=['POST'])
def create_call_route():
    data = request.get_json()
    call_id = create_call(data['description'])
    return jsonify({'id': call_id}), 201

@calls_bp.route('', methods=['GET'])
def get_calls():
    return jsonify(get_all_calls())

@calls_bp.route('/<int:call_id>/tags', methods=['POST'])
def assign_tag(call_id):
    data = request.get_json()
    assign_tag_to_call(call_id, data['tag_id'])
    return jsonify({'status': 'Tag assigned'}), 200

@calls_bp.route('/<int:call_id>/tags', methods=['GET'])
def get_tags_for_call(call_id):
    return jsonify(get_tags_for_call_db(call_id))

@calls_bp.route('/<int:call_id>/tasks', methods=['POST'])
def assign_task(call_id):
    data = request.get_json()
    assign_task_to_call(call_id, data['task_id'])
    return jsonify({'status': 'Task assigned'}), 200

@calls_bp.route('/<int:call_id>/tasks', methods=['GET'])
def get_call_tasks(call_id):
    return jsonify(get_tasks_for_call(call_id))
