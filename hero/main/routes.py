from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("layout.html")

@main.route("/about")
def about():
    return "About Page"
