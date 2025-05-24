from flask import Blueprint, jsonify
from app.services.database import get_all_users

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])
def fetch_users():
    return jsonify(get_all_users())
