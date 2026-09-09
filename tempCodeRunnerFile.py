from flask import Flask, request, jsonify, render_template
import time

app = Flask(__name__)

# Fast in-memory storage for bus coordinates
buses = {}

# Serve the Passenger Viewer page
@app.route('/')
def viewer():
    return render_template('viewer.html')

# Serve the Driver Transmitter page
@app.route('/driver-login')
def driver():
    return render_template('driver.html')

# API for drivers to send their location
@app.route('/api/location', methods=['POST'])
def update_location():
    data = request.json
    bus_id = data.get('bus_id')
    lat = data.get('lat')
    lng = data.get('lng')
    
    if bus_id and lat and lng:
        buses[bus_id] = {
            'lat': lat,
            'lng': lng,
            'timestamp': time.time()
        }
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid data"}), 400

# API for the passenger map to fetch all bus locations
@app.route('/api/buses', methods=['GET'])
def get_buses():
    # In a production app, you would filter out buses whose 
    # timestamps are too old (indicating they went offline)
    return jsonify(buses), 200

if __name__ == '__main__':
    # Run on all network interfaces so phones can connect
    app.run(debug=True, host='0.0.0.0', port=5000)