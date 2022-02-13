from flask import Flask

from api_bots import api_bots
from database import db_session

app = Flask(__name__)
app.register_blueprint(api_bots)


@app.teardown_appcontext
def close_session(exception=None):
    db_session.remove()
