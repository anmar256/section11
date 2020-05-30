from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help="This field cannot be blank!")
_user_parser.add_argument('password', type=str, required=True, help="This field cannot be blank!")


class UserRegister(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        print(data)
        if UserModel.find_by_username(data['username']):
            return {'message': "this username exists"}, 400

        # user = UserModel(data['username'], data['password'])
        user = UserModel(**data)
        user.save_to_db()

        return {'message': "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json(), 200
        return {'message': 'failed', 'detail': 'this user_id does not exists.'}, 404

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            try:
                user.delete_from_db()
                return {'message': 'ok', 'detail': 'user deleted successfully'}, 200
            except:
                return {'message': 'failed', 'detail': 'internal server error'}, 500
        return {'message': 'failed', 'detail': 'this user_id does not exists'}, 404


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        # this is what authenticate() function used to do
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            # identity= is what identity function used to do
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        return {'message': 'failed', 'detail': 'Username or Password is incorrect'}, 401
