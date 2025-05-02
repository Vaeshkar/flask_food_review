from flask import Flask # grab the class Flask from the flask module
from routes import auth_bp, restaurants_bp # grab the following blueprints from the routes directory
from routes.home import home_bp
 
def create_app():
    app = Flask(__name__, instance_relative_config=True)
 
    app.register_blueprint(auth_bp)
    app.register_blueprint(restaurants_bp)
    app.register_blueprint(home_bp)
 
    return app