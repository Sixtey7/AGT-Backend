from flask import Flask
from model.database import db
from routes.item_routes import item_api
from routes.category_routes import category_api
from routes.event_routes import event_api
from routes.export_routes import export_api
from flask_cors import CORS
import os

# create the flask app
app = Flask(__name__)


def init_sqlite():
    print('Standing up sqlite')

    if 'DB_LOC' in os.environ:
        location = os.environ['DB_LOC']
    else:
        print('location not set, using default of ./model/')
        location = 'model/'

    db_path = 'sqlite:///' + location + '/agt-backend.db'
    print('standing up sqlite with path: ' + db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_ECHO'] = True


def init_postgres():
    print('Standing up postgres')

    # READ in or default a bunch of config values
    if 'SERVER_URL' in os.environ:
        server_url = os.environ['SERVER_URL']
    else:
        print('server url not specified, assuming localhost')
        server_url = 'localhost'
    print('Using server url of: ' + server_url)

    if 'SERVER_PORT' in os.environ:
        server_port = os.environ['SERVER_PORT']
    else:
        print('server port not specified, assuming 5432')
        server_port = 5432
    print('using server port of: %d' % server_port)

    if 'DB_NAME' in os.environ:
        db_name = os.environ['DB_NAME']
    else:
        print('database name not specified, assuming agt_db')
        db_name = 'agt'
    print('using database name of: ' + db_name)

    if 'DB_USER' in os.environ:
        db_user = os.environ['DB_USER']
    else:
        print('db user not specified, assuming agt_user')
        db_user = 'agt_user'
    print('using db user of: ' + db_user)

    if 'DB_PASSWORD' in os.environ:
        db_password = os.environ['DB_PASSWORD']
    else:
        print('db password not specified, using default')
        db_password = 'password'

    # TODO
    db_path = 'postgresql+psycopg2://%s:%s@%s:%d/%s' % (db_user, db_password, server_url, server_port, db_name)
    print('built db string %s' % db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_ECHO'] = True


# add in CORS support
CORS(app, resources={r"/items/*": {"origins": "*"}})
CORS(app, resources={r"/categories/*": {"origins": "*"}})
CORS(app, resources={r"/events/*": {"origins": "*"}})
CORS(app, resources={r"/export/*": {"origins": "*"}})

app.register_blueprint(item_api, url_prefix="/items/")
app.register_blueprint(category_api, url_prefix="/categories/")
app.register_blueprint(event_api, url_prefix="/events/")
app.register_blueprint(export_api, url_prefix="/export/")

# SQLAlchemy config
if 'DB_TYPE' in os.environ:
    if os.environ['DB_TYPE'] == 'sqlite':
        init_sqlite()
    elif os.environ['DB_TYPE'] == 'postgres':
        init_postgres()
else:
    print('no database was specified, assuming sqlite')
    init_sqlite()

db.init_app(app)

db.app = app

# Create all of the tables
# Note: The below line comes back as not used, but its needed
import model.models
db.create_all()

app.run(host='0.0.0.0', port=5000, debug=True)



