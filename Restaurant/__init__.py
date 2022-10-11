from ast import main
from Restaurant import Routes
from Restaurant.Routes import routes
from flask import Flask
from .extensions import mongo
from .Routes.routes import main
def create_app():
    
    app = Flask(__name__)
    
    app.config["MONGO_URI"] = "mongodb+srv://Rohit:edaS1fywFhS9bUqk@cluster0.f9hrdsc.mongodb.net/pizza_house?retryWrites=true&w=majority"
    
    app.register_blueprint(main)
    mongo.init_app(app)
    
    
    return app