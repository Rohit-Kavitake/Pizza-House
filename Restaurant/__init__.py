from flask import Blueprint, Flask, jsonify, make_response, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from celery import Celery
from flask_celery import make_celery
from .extensions import *

broker_url='amqp://localhost//'
backend_url='mongodb+srv://Rohit:edaS1fywFhS9bUqk@cluster0.f9hrdsc.mongodb.net/pizza_house?retryWrites=true&w=majority'

   
app = Flask(__name__)

app.config['CELERY_BROKER_URL']='amqp://localhost//'
app.config['CELERY_RESULT_BACKEND']='mongodb+srv://Rohit:edaS1fywFhS9bUqk@cluster0.f9hrdsc.mongodb.net/pizza_house?retryWrites=true&w=majority'
celery=make_celery(app)

app.config["MONGO_URI"] = "mongodb+srv://Rohit:edaS1fywFhS9bUqk@cluster0.f9hrdsc.mongodb.net/pizza_house?retryWrites=true&w=majority"

main = Blueprint("main", __name__)
mongo = PyMongo(app)
  


@main.route("/welcome")     #Task 1
def welcome():
    return("Welcome to Pizza House"),200


# @main.route("/order", methods = ["POST"])      #Task 2
# def orders():
#     orderData  = request.get_json(force=True)
#     new_order = mongo.db.orders.insert_one(orderData).inserted_id
#     return make_response(jsonify(message = "success",ID = str(new_order))), 201


@main.route("/getorders")  #Task3.1
def get_order():
    orderHistory = mongo.db.orders.find()
    return make_response((dumps(orderHistory))),200



@main.route("/getorders/<order_id>")    #Task3.2
def getOrder(order_id):
    order = mongo.db.orders.find_one({'_id': ObjectId(order_id)})
    return make_response((dumps(order))),200

@main.route("/order", methods = ["POST"])   #Task 4
def addOrder():
    orderData  = request.get_json(force=True)
    add_order.delay(orderData)
    
@celery.task(name="app.addSubjects")
def add_order(orderData):
    new_order = mongo.db.orders.insert_one(orderData).inserted_id
    return make_response(jsonify(message = "success",ID = str(new_order))), 201
    
app.register_blueprint(main)
