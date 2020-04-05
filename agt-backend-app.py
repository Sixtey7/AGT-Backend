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
# read in the location of the database
if 'DB_LOC' in os.environ:
    db_location = os.environ['DB_LOC']
    print('DB Location was set, using location: ' + db_location)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_location + '/agt-backend.db'
else:
    print('location not set, using default of ./model/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model/agt-backend.db'

app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

db.app = app

# Create all of the tables
# Note: The below line comes back as not used, but its needed
import model.models
db.create_all()

app.run(host='0.0.0.0', port=5000, debug=True)
