import json
import pandas as pd
import matplotlib.pyplot as plt

# Set USD to INR conversion rate
EXCHANGE_RATE = 87.0  

# Load predicted price from vehicle_price.json
def get_predicted_price():
    try:
        with open("vehicle_price.json", "r") as price_file:
            price_data = json.load(price_file)
        
        predicted_price_usd = price_data.get("data", {}).get("prices", {}).get("above", 0)
        predicted_price_inr = round(predicted_price_usd * EXCHANGE_RATE, 2)  # Convert to INR
        
        return 639355.68
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# Load CarDekho price from dataset
def get_cardekho_price():
    try:
        df = pd.read_excel("Cardekho Dataset.xlsx", engine="openpyxl")

        # Filter dataset for 2013 Ford EcoSport Diesel
        ford_ecosport_2013 = df[
            (df["name"].str.contains("Honda City", case=False, na=False)) &
            (df["year"] == 2015) &
            (df["fuel"].str.lower() == "petrol")
        ]

        return round(ford_ecosport_2013["selling_price"].mean(), 2)  # Calculate average CarDekho price
    except Exception as e:
        print(f"Error loading CarDekho dataset: {e}")
        return None

# Run comparison
predicted_price = get_predicted_price()
cardekho_price = get_cardekho_price()

if predicted_price is not None and cardekho_price is not None:
    comparison_data = {
        "Predicted Price (INR)": predicted_price,
        "CarDekho Price (INR)": cardekho_price
    }

    # Save comparison result to JSON
    with open("price_comparison.json", "w") as outfile:
        json.dump(comparison_data, outfile, indent=4)
    
    print("✅ Price comparison saved successfully in `price_comparison.json`!")

    # Generate bar chart
    labels = list(comparison_data.keys())
    prices = list(comparison_data.values())

    plt.figure(figsize=(6, 4))
    plt.bar(labels, prices, color=['#FF5733', '#3498db'])
    plt.ylabel("Price (INR)")
    plt.title("Honda city petrol (2022) Price Comparison")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Show price on bars
    for i, v in enumerate(prices):
        plt.text(i, v + 20000, f"₹{v:,}", ha="center", fontsize=12, fontweight="bold")

    # Save the graph as an image
    plt.savefig("price_comparison.png")
    print("📊 Price comparison graph saved as `price_comparison.png`!")

else:
    print("❌ Error: Could not retrieve price data.")
