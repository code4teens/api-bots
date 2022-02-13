from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from database import db_session
from models import Bot, Cohort, User
from schemata import BotSchema

api_bots = Blueprint('api_bots', __name__)


@api_bots.route('/bots')
def get_bots():
    bots = Bot.query.order_by(Bot.id).all()
    data = BotSchema(many=True).dump(bots)

    return jsonify(data), 200


@api_bots.route('/bots', methods=['POST'])
def create_bot():
    keys = [
        'id',
        'name',
        'discriminator',
        'display_name',
        'user_id',
        'cohort_id',
        'msg_id'
    ]

    if sorted([key for key in request.json]) == sorted(keys):
        id = request.json.get('id')
        name = request.json.get('name')
        discriminator = request.json.get('discriminator')
        existing_bot_1 = Bot.query.filter_by(id=id).one_or_none()
        existing_bot_2 = Bot.query.filter_by(name=name)\
            .filter_by(discriminator=discriminator)\
            .one_or_none()

        if existing_bot_1 is None and existing_bot_2 is None:
            user_id = request.json.get('user_id')
            cohort_id = request.json.get('cohort_id')
            user = User.query.filter_by(id=user_id).one_or_none()
            cohort = Cohort.query.filter_by(id=cohort_id).one_or_none()

            if user is not None and cohort is not None:
                bot_schema = BotSchema()

                try:
                    bot = bot_schema.load(request.json)
                except Exception as _:
                    data = {
                        'title': 'Bad Request',
                        'status': 400,
                        'detail': 'Some values failed validation'
                    }

                    return data, 400
                else:
                    db_session.add(bot)

                    try:
                        db_session.commit()
                    except exc.IntegrityError as _:
                        data = {
                            'title': 'Bad Request',
                            'status': 400,
                            'detail': 'Some values failed validation'
                        }

                        return data, 400
                    else:
                        data = {
                            'title': 'Created',
                            'status': 201,
                            'detail': f'Bot {id} created'
                        }

                        return data, 201
            else:
                data = {
                    'title': 'Bad Request',
                    'status': 400,
                    'detail': 'User or cohort does not exist'
                }

                return data, 400
        else:
            data = {
                'title': 'Conflict',
                'status': 409
            }

            if existing_bot_1 is not None:
                data['detail'] = f'Bot {id} already exists'
            else:
                data['detail'] = f'Bot {name}#{discriminator} already exists'

            return data, 409
    else:
        data = {
            'title': 'Bad Request',
            'status': 400,
            'detail': 'Missing some keys or contains extra keys'
        }

        return data, 400


@api_bots.route('/bots/<int:id>')
def get_bot(id):
    bot = Bot.query.filter_by(id=id).one_or_none()

    if bot is not None:
        data = BotSchema().dump(bot)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Bot {id} not found'
        }

        return data, 404


@api_bots.route('/bots/<int:id>', methods=['PUT'])
def update_enrolment(id):
    keys = [
        'name',
        'discriminator',
        'display_name',
        'user_id',
        'cohort_id',
        'msg_id'
    ]

    if all(key in keys for key in request.json):
        existing_bot = Bot.query.filter_by(id=id).one_or_none()

        if existing_bot is not None:
            bot_schema = BotSchema()

            try:
                bot = bot_schema.load(request.json)
            except Exception as _:
                data = {
                    'title': 'Bad Request',
                    'status': 400,
                    'detail': 'Some values failed validation'
                }

                return data, 400
            else:
                bot.id = existing_bot.id
                db_session.merge(bot)

                try:
                    db_session.commit()
                except exc.IntegrityError as _:
                    data = {
                        'title': 'Bad Request',
                        'status': 400,
                        'detail': 'Some values failed validation'
                    }

                    return data, 400
                else:
                    data = bot_schema.dump(existing_bot)

                    return data, 200
        else:
            data = {
                'title': 'Not Found',
                'status': 404,
                'detail': f'Bot {id} not found'
            }

            return data, 404
    else:
        data = {
            'title': 'Bad Request',
            'status': 400,
            'detail': 'Missing some keys or contains extra keys'
        }

        return data, 400


@api_bots.route('/bots/<int:id>', methods=['DELETE'])
def delete_bot(id):
    bot = Bot.query.filter_by(id=id).one_or_none()

    if bot is not None:
        db_session.delete(bot)
        db_session.commit()
        data = {
            'title': 'OK',
            'status': 200,
            'detail': f'Bot {id} deleted'
        }

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Bot {id} not found'
        }

        return data, 404
