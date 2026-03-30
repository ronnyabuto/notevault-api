from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models import User


def current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return db.session.get(User, user_id)


class Signup(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return {'error': 'Username and password are required.'}, 422

        if User.query.filter_by(username=username).first():
            return {'error': 'Username already taken.'}, 422

        try:
            user = User(username=username)
            user.password_hash = password
            db.session.add(user)
            db.session.commit()
        except ValueError as e:
            return {'error': str(e)}, 422

        session['user_id'] = user.id
        return user.to_dict(), 201


class CheckSession(Resource):
    def get(self):
        user = current_user()
        if not user:
            return {'error': 'Unauthorized — please log in.'}, 401
        return user.to_dict(), 200


class Login(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get('username', '').strip()
        password = data.get('password', '')

        user = User.query.filter_by(username=username).first()
        if not user or not user.authenticate(password):
            return {'error': 'Invalid username or password.'}, 401

        session['user_id'] = user.id
        return user.to_dict(), 200


class Logout(Resource):
    def delete(self):
        if not session.get('user_id'):
            return {'error': 'Unauthorized — no active session.'}, 401
        session.pop('user_id', None)
        return {}, 204


api.add_resource(Signup, '/signup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
