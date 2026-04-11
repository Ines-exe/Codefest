from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route("/donate", methods =["GET", "POST"])
def donate():
    if request.method == "POST":

        address= request.form.get("address")
        site_name= request.form.get("site_name")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        category = request.form.get("category")
        days = request.form.get("days")
        start_time = request.form.get("open_time")
        close_time = request.form.get("close_time")
        return "Your request has been made."
    return render_template("donate.html")

@app.route("/login")
def login():
        return render_template("login.html")

@app.route("/signup")
def signup():
        return render_template("signup.html")



if __name__=="__main__":
    app.run(debug=True)