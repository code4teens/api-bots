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
