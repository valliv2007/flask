import config
from flask_restful import Api
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy, get_debug_queries
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'Flask'})
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/greeting', methods=['POST'])
def greeting():
    name = request.form.get('name')
    if not name:
        return "Fill the form", 400
    return render_template('greeting.html', name=name)


app.debug = True


def sql_debug(response):
    queries = list(get_debug_queries())
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration

    print("=" * 80)
    print('SQL Queries- {0} Oueries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    print("=" * 80)
    return response


app.after_request(sql_debug)

from src import routes
from src.database import models
from src.tests import test_actors
