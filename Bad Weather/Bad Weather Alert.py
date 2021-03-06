import os
import requests
from twilio.rest import Client

your_phone_number = input("Enter Your Phone Number:")


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

api_key = "YOUR API KEY HERE"  # Enter Your API Key here!
api_endpoint = "https://api.openweathermap.org/data/2.5/onecall"

weather_params = {
	"lat": 34.385204,
	"lon": 132.455292,
	"appid": api_key,
	"exclude": "current,minutely,daily"
}

will_rain = False

connection = requests.get(api_endpoint, params=weather_params)
connection.raise_for_status()
weather_data = connection.json()
# print(f"Weather: {connection.json()['current']['weather']}")
weather_slice = weather_data['hourly'][:12]

for hour_data in weather_slice:
	condition_code = (hour_data["weather"][0]["id"])  # in [weather] zeroth element is a dictionary
	#                                                       and 'id' is part of that dictionary.
	if condition_code < 700:
		will_rain = True


if will_rain:
	client = Client(account_sid, auth_token)
	message = client.messages \
		.create(
		body="It's going to rain today. Don't forget to bring an umbrella.",
		from_="+19705368315",
		to=f"{your_phone_number}"
	)
	print(message.status)
