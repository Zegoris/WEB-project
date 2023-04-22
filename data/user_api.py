from flask import jsonify, request, Blueprint

from data import db_session
from data.users import User

blueprint = Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_quotes():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    return jsonify(
        {'users':
             [item.to_dict(only=('id', 'email', 'user',
                                 'hashed_password', 'type', 'current_quote')) for item in user]
         }
    )

@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_quote(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'email', 'user',
                                        'hashed_password', 'type', 'current_quote'))
        }
    )

@blueprint.route('/api/users', methods=['POST'])
def create_quote():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['email', 'user',
                  'password', 'type', 'current_quote']):
        return jsonify({'error': 'Bad request'})
    user = User(
        email=request.json['email'],
        user=request.json['user'],
        type=request.json['type'],
        current_quote=request.json['current_quote']
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_quote(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def change_job(user_id):
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'Not found'})
    user.type = request.json['type']
    db_sess.commit()
    return jsonify({'success': 'OK'})

