from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
import os
import requests

app = Flask(__name__)

# Load Twilio & Google API credentials securely (Replace with environment variables)
TWILIO_SID = os.getenv("TWILIO_SID", "your_twilio_sid")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_twilio_auth_token")
TWILIO_PHONE = os.getenv("TWILIO_PHONE", "your_twilio_phone_number")
EMERGENCY_CONTACT = os.getenv("EMERGENCY_CONTACT", "+91XXXXXXXXXX")  # Replace with an actual contact

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "your_google_maps_api_key")

# Function to send emergency alert via Twilio
def send_alert(message, lat=None, lon=None):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    alert_msg = message
    if lat and lon:
        alert_msg += f" 📍 Location: https://www.google.com/maps?q={lat},{lon}"

    client.messages.create(
        body=alert_msg,
        from_=TWILIO_PHONE,
        to=EMERGENCY_CONTACT
    )

# AI-based Incident Detection (Dummy Function)
def detect_incident(sensor_data):
    return sensor_data.get("accident") or sensor_data.get("harassment")

# Vehicle Speed & Direction Detection (Dummy Data)
def detect_vehicle_info():
    return {"speed": "60 km/h", "direction": "North-East"}

@app.route("/")
def index():
    return render_template("index.html")

# Endpoint to check for incidents and send alerts
@app.route("/incident_status", methods=["POST"])
def check_incident():
    data = request.json
    if detect_incident(data):
        send_alert("🚨 Emergency detected! Immediate action required.")
        return jsonify({"status": "alert sent"})
    return jsonify({"status": "safe"})

# Endpoint to get vehicle status
@app.route("/vehicle_status", methods=["GET"])
def vehicle_status():
    return jsonify(detect_vehicle_info())

# Google Maps Route API
@app.route("/get_route", methods=["GET"])
def get_route():
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    
    if not origin or not destination:
        return jsonify({"error": "Missing origin or destination"}), 400
    
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Failed to fetch route"}), response.status_code

# Endpoint to send live location alert
@app.route("/send_alert", methods=["POST"])
def send_location_alert():
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude and longitude:
        send_alert("📡 Live location shared!", latitude, longitude)
        return jsonify({"status": "location shared"})
    return jsonify({"error": "Invalid location data"}), 400

if __name__ == "__main__":
    app.run(debug=True)
