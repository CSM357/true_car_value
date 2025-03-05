import requests

url = "https://rto-vehicle-information-india.p.rapidapi.com/getVehicleInfo"

payload = {
	"vehicle_no": "22BH6517A",
	"consent": "Y",
	"consent_text": "I hereby give my consent for Eccentric Labs API to fetch my information"
}
headers = {
	"x-rapidapi-key": "6c449e9428msh82fe38348275a97p17e402jsn3a259d012059",
	"x-rapidapi-host": "rto-vehicle-information-india.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())