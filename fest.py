from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from dotenv import load_dotenv
import os
import csv
from groq import Groq

app = Flask(__name__)

FAKEUSERS = {
     "test@gmail.com": ["password","user"],
     "test2@gmail.com": ["password","donator"]
}

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

    return render_template("donate.html",succes = True)

@app.route("/user", methods = ["GET","POST"])
def user():
        import pandas as pd
        #import google as genai
        from geopy.distance import geodesic
        from geopy.geocoders import Nominatim


        if request.method == "POST":
            print("POST received!")
            print(request.json)
            #getting the coordinates from the user's location from the .js
            lat = request.json.get("lat")
            long = request.json.get("long")
            user_coordinates = (lat, long)
            date = request.json.get("date")
            time = request.json.get("time")
            user_category = request.json.get("user_category")


            #getting the data from the user frm the .html and storing some in a dictionary
            max_distance = request.json.get("max_distance")

            user_data = {
                "date": date,
                "time": time,
                "user_category": user_category
            }

            #making the pandas to read the csv files
            donations = pd.read_csv("donations.csv").head(20)
            data = pd.read_csv("free_meal_sites.csv").head(20)
            print("CSVs loaded")

            #intializing nominatim
            geolocator = Nominatim(user_agent="my_service_locator", timeout= 5)
            
            #filtering the data csv to just locations in the users preferred distance
            events_in_range = []
            
            #looping through both data files
            """for dataFile in [data,donations]:
                #looping in one file
                for row in dataFile.itertuples():
                    event_address = row.address
                    try:
                        event_lat = float(row.x)
                        event_long = float(row.y)
                        event_coordinates = (event_lat, event_long)
                        event_location = geolocator.geocode(event_address)
                    except:
                         continue

                    if event_location:
                        event_coordinates = (event_location.latitude, event_location.longitude)

                        #comparing the distance between the two
                        distance = geodesic(event_coordinates,user_coordinates).miles
                        #adding the event to the list of events in range if it is in range
                        if distance <= float(max_distance):

                            #turning the row into a dictionary
                            row_dict = row._asdict()

                            #adding the coordinates to the dictionary
                            row_dict["lat"] = event_coordinates[0]
                            row_dict["long"] = event_coordinates[1]

                            #appending the dictionary to the events list
                            events_in_range.append(row_dict)

                    print("geocoding done, events in range:", len(events_in_range))"""
            #changed code...idk why tho i forgot
            for dataFile in [data, donations]:
                for row in dataFile.itertuples():
                    try:
                        event_lat = float(row.x)
                        event_long = float(row.y)
                        event_coordinates = (event_lat, event_long)
                        distance = geodesic(event_coordinates, user_coordinates).miles
                        if distance <= float(max_distance):
                            row_dict = row._asdict()
                            row_dict["lat"] = event_lat
                            row_dict["long"] = event_long
                            events_in_range.append(row_dict)
                    except:
                        continue



            #intializing gemini and sending the data to it
            client = Groq(api_key = os.getenv("GROQ_API_KEY"))

            message = f"""Based on the user's needs: {user_data} and the resource sites within the user's distance: {events_in_range} recommend the sites that fit them the best and why.
            Your recommendation should only be returned as a JSON array like this format, no other format:
            [
                {{"site_name":".....", "address":"....", "reason":"....", "lat":"....","long":"...."}},
                {{"site_name":".....", "address":"....", "reason":"....", "lat":"....","long":"...."}}
            ]   
            """
            print("sending to groq")
            response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": message}]
            )
            print("groq done")
            recommendations = response.choices[0].message.content

            print("recommendations:", recommendations)
            return jsonify({"recommendations":recommendations})

        return render_template("user.html")

@app.route("/login", methods = ["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email in FAKEUSERS and FAKEUSERS[email][0] == password:
            role = FAKEUSERS[email][1]
            if role == "user":
                 return render_template("user.html")
            
            elif role == "donator":
                 return render_template("donate.html")
                
        else: return "FAIL"
    
    return render_template("login.html")

@app.route("/index")
def main():
        return render_template("index.html")

@app.route("/signupDonator")
def signupDonator():
        return render_template("signupDonator.html")

@app.route("/signupUser")
def signupUser():
        return render_template("signupUser.html")

#home page
@app.route("/")
def home():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)