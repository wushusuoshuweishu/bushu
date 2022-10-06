# -*- coding: utf-8 -*-

from app.checkers import register_params_check
from app.services import UserService
from app.utils import generate_jwt
from flask import Blueprint, g, jsonify, request
from flasgger import swag_from
from .login_required import login_required

bp = Blueprint(
    'user',
    __name__,
    template_folder='../templates'
)

service = UserService()


@bp.route('/api/v1/user', methods=['GET'])
@swag_from('swagger/user.yml')
@login_required
def get_user_info():
    """
    获取当前登录用户信息
    """
    user, result = service.get_user(g.user_id)
    if result:
        return jsonify({
            "id":       user.id,
            "username": user.username,
            "nickname": user.nickname,
            "created":  user.created,
            "url": user.url,
            "mobile": user.mobile,
        }), 200
    else:
        return jsonify({'message': user}), 500


@bp.route('/api/v1/user/<int:userId>', methods=['GET'])
@swag_from('swagger/user-id.yml')
@login_required
def get_user_info_by_id(userId):
    """
    获取指定用户信息
    """
    user, result = service.get_user(userId)
    if result:
        return jsonify({
            "id":       user.id,
            "nickname": user.nickname,
            "created":  user.created,
        }), 200
    else:
        return jsonify({'message': user}), 500


@bp.route('/api/v1/login', methods=['PATCH'])
@swag_from('swagger/login.yml')
def login():
    """
    登录
    """
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "bad arguments"}), 400
        user, result = service.get_user_with_pass(
            content['username'], content['password'])

        if result:
            jwt = generate_jwt({
                "user_id": user.id,
                "nickname": user.nickname
            })
            return jsonify({
                "jwt":      jwt,
                "userId": user.id,
                "username": user.username,
                "nickname": user.nickname,
            }), 200
        else:
            return jsonify({'message': user}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400


@bp.route('/api/v1/logout', methods=['PATCH'])
@swag_from('swagger/logout.yml')
@login_required
def logout():
    """
    登出
    本次作业中简化，不做任何操作
    """
    return jsonify({'message': "ok"}), 200


@bp.route('/api/v1/register', methods=['POST'])
@swag_from('swagger/register.yml')
def register_user():
    """
    用户注册
    """
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "bad arguments"}), 400
        key, passed = register_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        result = service.create_user(content['username'],
                                     content['password'],
                                     content['nickname'],
                                     content['url'],
                                     content['mobile'],
                                     content['magic_number']
                                     )

        if result:
            return jsonify({'message': "ok"}), 200
        else:
            return jsonify({'message': "error"}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400