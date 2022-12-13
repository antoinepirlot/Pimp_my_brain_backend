from flask import Blueprint, jsonify, request

from Exceptions.WebExceptions.BadRequestException import BadRequestException
from services.UsersService import UsersService
from utils.security import prevent_xss

users_service = UsersService()

route = Blueprint("users", __name__)


# #########
# ###GET###
# #########
@route.route('', methods=['GET'])
def get_users():
    result = users_service.get_users()
    users = []
    for user in result:
        users.append(user.convert_to_json())

    return users


@route.route('/<int:id_user>', methods=['GET'])
def get_user_by_id(id_user):
    if id_user is None or id_user <= 0:
        raise BadRequestException("ID of the user is not mentioned or negative")
    result = users_service.get_users_by_id(id_user)
    return result.convert_to_json(), 200


@route.route('teacher/<int:id_teacher>', methods=['GET'])
def get_teacher_by_id(id_teacher):
    if id_teacher is None or id_teacher <= 0:
        raise BadRequestException("ID of the teacher is not mentioned or negative")
    result = users_service.get_teacher_by_id(id_teacher)
    return result.convert_to_json()


@route.route('/<string:email>', methods=['GET'])
def get_user_by_email(email):
    if email is None or len(email) == 0:
        raise BadRequestException("email is not mentioned or empthy")
    email = prevent_xss(email)
    result = users_service.get_users_by_email(email)
    return result.convert_to_json()


@route.route('/pseudo/<string:pseudo>', methods=['GET'])
def get_user_by_pseudo(pseudo):
    pseudo = prevent_xss(pseudo)
    if pseudo is None or pseudo.strip() == 0:
        raise BadRequestException("pseudo is not mentioned or empthy")
    result = users_service.get_users_by_pseudo(pseudo)
    return result.convert_to_json()


# ########
# ##POST##
# ########
@route.route('', methods=['POST'])
def add_user():
    users_service.sing_in_user(prevent_xss(request.json))
    return jsonify({'user': 'user created'})
