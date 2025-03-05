import os
import json
import subprocess
from flask import Flask, request, jsonify, render_template
from license_plate_recognition import recognize_license_plate  

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_vehicle_info(license_plate):
    """Runs test.py to fetch vehicle details"""
    try:
        result = subprocess.run(
            ['python', 'test.py', license_plate],
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running test.py: {e.stderr.decode()}")
        return False

def get_vehicle_price(maker, model, year):
    """Runs price.py to fetch original vehicle price"""
    try:
        result = subprocess.run(
            ['python', 'price.py', maker, model, year], 
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running price.py: {e.stderr.decode()}")
        return False

def calculate_discounted_price():
    """Runs calculateprice.py to fetch discounted price"""
    try:
        result = subprocess.run(
            ['python', 'calculateprice.py'], 
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running calculateprice.py: {e.stderr.decode()}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize_lp', methods=['POST'])
def recognize_license_plate_endpoint():
    lp_image = request.files.get('lp_image')
    if not lp_image:
        return jsonify({'status': False, 'error': 'No license plate image uploaded'}), 400
    
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], lp_image.filename)
    lp_image.save(image_path)
    license_plate_text = recognize_license_plate(image_path)
    
    if not license_plate_text:
        return jsonify({'status': False, 'error': 'No license plate detected'}), 400
    
    success = get_vehicle_info(license_plate_text)
    if not success:
        return jsonify({'status': False, 'error': 'Failed to fetch vehicle information'}), 400
    
    try:
        with open('vehicle_info.json') as json_file:
            vehicle_info = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({'status': False, 'error': 'Vehicle info file error'}), 400
    
    return jsonify({'status': True, 'license_plate': license_plate_text, 'vehicle_info': vehicle_info})

@app.route('/get-vehicle-details', methods=['GET'])
def get_vehicle_detail():
    try:
        with open("vehicle_info.json", 'r') as fs:
            data = json.load(fs)
        return jsonify({'status': True, 'success': data}), 200
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({'status': False, 'error': 'Vehicle details not found'}), 400

@app.route('/get-original-price', methods=['GET'])
def get_original_price():
    """Returns original price from vehicle_price.json in INR"""
    try:
        with open("vehicle_price.json", 'r') as fs:
            price_data = json.load(fs)
        
        # Extract the original price in USD
        original_price_usd = price_data.get("data", {}).get("prices", {}).get("above", 0)

        # Convert to INR (Fixed exchange rate: 1 USD = 87 INR)
        exchange_rate = 83.0
        original_price_inr = round(original_price_usd * exchange_rate, 2)

        return jsonify({'status': True, 'original_price': original_price_inr*2}), 200
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({'status': False, 'error': 'Price details not found'}), 400



@app.route('/get-discounted-price', methods=['GET'])
def get_discounted_price():
    """Returns discounted price after running calculateprice.py"""
    success = calculate_discounted_price()
    if success:
        try:
            with open("discounted_price.json", 'r') as fs:
                price_data = json.load(fs)
            return jsonify({'status': True, 'discounted_price': price_data.get("discounted_price", "N/A")}), 200
        except (FileNotFoundError, json.JSONDecodeError):
            return jsonify({'status': False, 'error': 'Discounted price not found'}), 400
    return jsonify({'status': False, 'error': 'Failed to calculate discounted price'}), 400

if __name__ == '__main__':
    app.run(debug=True)
