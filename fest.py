from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import csv
from groq import Groq

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
        open_time = request.form.get("open_time")
        close_time = request.form.get("close_time")

        with open("donations.csv","a", newline ="") as file:
              writer = csv.writer(file)
              writer.writerow([site_name, address, phone_number,category, days,open_time, close_time])

        return "Your request has been made."

    return render_template("donate.html")

@app.route("/user", methods = ["GET","POST"])
def user():
        import pandas as pd
        import google.generativeai as googleAi
        from geopy.distance import geodesic
        from geopy.geocoders import Nominatim


        if request.method == "POST":
            #getting the coordinates from the user's location from the .js
            lat = request.json.get("lat")
            long = request.json.get("long")
            user_coordinates = (lat, long)

            #getting the data from the user frm the .html and storing some in a dictionary
            max_distance = request.form.get("max_distance")

            user_data = {
                "max_distance" : request.form.get("max_distance"),
                "date": request.form.get("date"),
                "time": request.form.get("time"),
                "user_category": request.form.get("user_category")
            }

            #making the pandas to read the csv files
            donations = pd.read_csv("donations.csv")
            data = pd.read_csv("free_meal_sites.csv")
            
            #intializing nominatim
            geolocator = Nominatim(user_agent="my_service_locator")
            
            #filtering the data csv to just locations in the users preferred distance
            events_in_range = []
            
            #looping through both data files
            for dataFile in [data,donations]:
                #looping in one file
                for index, row in dataFile.itertuples():

                    event_address = row.address
                    event_location = geolocator.geocode(event_address)

                    if event_location:
                        event_coordinates = (event_location.latitude, event_location.longitude)

                        #comparing the distance between the two
                        distance = geodesic(event_coordinates,user_coordinates).miles
                        if distance <= float(user_data["max_distance"]):
                             events_in_range.append(row)

            #intializing gemini
            googleAi.configure(api_key = os.getenv("GEMINI_API_KEY"))

            #sending the data to Gemini


        return render_template("user.html")

@app.route("/login")
def login():
        return render_template("login.html")

@app.route("/signup")
def signup():
        return render_template("signup.html")

@app.route("/index")
def main():
        return render_template("index.html")



if __name__=="__main__":
    app.run(debug=True)