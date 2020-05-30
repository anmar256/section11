import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank!")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
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
