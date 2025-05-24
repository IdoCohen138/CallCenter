from flask import Blueprint, request, jsonify
from app.services.database import get_user_by_username

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = get_user_by_username(data.get('username'))
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404
