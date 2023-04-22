from flask import jsonify, request, Blueprint

from data import db_session
from data.mixed import Mixed

blueprint = Blueprint(
    'quote_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/quotes', methods=['GET'])
def get_quotes():
    db_sess = db_session.create_session()
    quotes = db_sess.query(Mixed).all()
    return jsonify(
        {'quotes':
             [item.to_dict(only=('id', 'quote', 'person', 'work')) for item in quotes]
         }
    )

@blueprint.route('/api/quotes/<int:quote_id>', methods=['GET'])
def get_one_quote(quote_id):
    db_sess = db_session.create_session()
    quote = db_sess.query(Mixed).get(quote_id)
    if not quote:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'quote': quote.to_dict(only=('id', 'quote', 'person', 'work'))
        }
    )

@blueprint.route('/api/quotes', methods=['POST'])
def create_quote():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'quote', 'person', 'work']):
        return jsonify({'error': 'Bad request'})
    if db_sess.query(Mixed).filter(Mixed.id == request.json["id"]).first():
        return jsonify({'error': 'Id already exists'})
    quote = Mixed(
        id=request.json["id"],
        quote=request.json['quote'],
        person=request.json['person'],
        work=request.json['work']
    )
    db_sess.add(quote)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    db_sess = db_session.create_session()
    quote = db_sess.query(Mixed).get(quote_id)
    if not quote:
        return jsonify({'error': 'Not found'})
    db_sess.delete(quote)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/quotes/<int:quote_id>', methods=['PUT'])
def change_job(quote_id):
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    quote = db_sess.query(Mixed).filter(Mixed.id == quote_id).first()
    if not quote:
        return jsonify({'error': 'Not found'})
    quote.quote = request.json['quote']
    quote.person = request.json['person']
    quote.work = request.json['work']
    db_sess.commit()
    return jsonify({'success': 'OK'})

