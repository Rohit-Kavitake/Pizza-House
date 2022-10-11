from flask import Blueprint

main = Blueprint("main", __name__)


@main.route("/welcome")
def welcome():
    return("Welcome to Pizza House")