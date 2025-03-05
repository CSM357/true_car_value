import requests
import json

# Define API details
url = "https://vehicle-pricing-api.p.rapidapi.com/get%2Bvehicle%2Bvalue"

# API query parameters
querystring = {
    "maker": "HONDA",
    "model": "CITY",
    "year": "2022"
}

# API headers
headers = {
    "x-rapidapi-key": "6c449e9428msh82fe38348275a97p17e402jsn3a259d012059",
    "x-rapidapi-host": "vehicle-pricing-api.p.rapidapi.com"
}

def fetch_vehicle_price(url, headers, querystring):
    try:
        # Make the API request
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the response JSON
        data = response.json()

        # Print the response JSON
        print(data)
        
        # Save the output to a JSON file
        with open("vehicle_price.json", "w") as outfile:
            json.dump(data, outfile, indent=4)
        
        print("Vehicle price data saved successfully.")
    
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"Error fetching vehicle price: {e}")

# Fetch vehicle price data
fetch_vehicle_price(url, headers, querystring)
