import json
from datetime import datetime
import math

# Load vehicle price data
with open("vehicle_price.json", "r") as price_file:
    price_data = json.load(price_file)

# Load vehicle info data
with open("vehicle_info.json", "r") as info_file:
    vehicle_info = json.load(info_file)

# Extract relevant details
base_price_usd = price_data["data"]["prices"]["above"]  # Base market price in USD
registration_date = vehicle_info["data"]["registration_date"]  # Registration date
fuel_type = vehicle_info["data"]["fuel_type"].upper()  # Convert fuel type to uppercase for consistency

# Convert registration date to year
registration_year = int(datetime.strptime(registration_date, "%d-%b-%Y").year)
current_year = datetime.now().year
vehicle_age = current_year - registration_year  # Calculate vehicle age

# Set depreciation rates
depreciation_rates = {
    "DIESEL": 0.09,  # 9% per year
    "PETROL": 0.10   # 10% per year
}

# Calculate estimated price after depreciation
if fuel_type in depreciation_rates:
    depreciation_rate = depreciation_rates[fuel_type]
    estimated_price_usd = base_price_usd * math.pow((1 - depreciation_rate), vehicle_age)
else:
    estimated_price_usd = base_price_usd  # If unknown fuel type, keep base price

# Set a fixed exchange rate (1 USD to INR)
usd_to_inr_rate = 83.0  # Example: 1 USD = 83 INR (update this manually as needed)

# Convert estimated price to INR
estimated_price_inr = round(estimated_price_usd * usd_to_inr_rate, 2)

# Save the discounted price to a JSON file
discounted_price_data = {"discounted_price": estimated_price_inr*2}
with open("discounted_price.json", "w") as outfile:
    json.dump(discounted_price_data, outfile, indent=4)

print("Discounted price saved successfully.")