# from flask import Blueprint, jsonify
# from app.services.database import get_all_users

# users_bp = Blueprint('users', __name__)

# @users_bp.route('/', methods=['GET'])
# def fetch_users():
#     print("📍 get_all_users called")
#     return jsonify(get_all_users())

from flask import request, jsonify, Blueprint

users_bp = Blueprint('users', __name__)

@users_bp.route("/check", methods=["GET"])
def check_request_info():
    return jsonify({
        "scheme": request.scheme,
        "url": request.url,
        "headers": dict(request.headers)
    })
