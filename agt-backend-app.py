from flask import Flask
from model.database import db
from routes.item_routes import item_api
from routes.category_routes import  category_api
from flask_cors import CORS

# create the flask app
app = Flask(__name__)

# add in CORS support
CORS(app, resources={r"/items/*": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/categories/*": {"origins": "http://localhost:8080"}})

app.register_blueprint(item_api, url_prefix="/items/")
app.register_blueprint(category_api, url_prefix="/categories/")
# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model/agt-backend.db'
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

db.app = app

# Create all of the tables
# Note: The below line comes back as not used, but its needed
import model.models
db.create_all()

app.run(port=5000, debug=True)