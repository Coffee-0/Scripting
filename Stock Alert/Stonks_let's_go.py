import requests
from twilio.rest import Client
import os

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_ENDPOINT_KEY = "f4d2bced11474f1eb5d0feb0f8cbc9c3"

news_params = {
	"apiKey": NEWS_ENDPOINT_KEY,
	"qInTitle": "TSLA",

}


stock_params = {
	"function": "TIME_SERIES_DAILY",
	"symbol": "TSLA",
	"apikey": "ZZH3DTN0JDE637DG"
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]

# Yesterdays data
yesterday_closing_price = data_list[0]['4. close']

# Day before yesterdays data
day_before_yesterday_closing_price = data_list[1]['4. close']

difference = abs(float(day_before_yesterday_closing_price) - float(yesterday_closing_price))

diff_percent = (difference / float(yesterday_closing_price)) * 100

if diff_percent > 0.5:
	news_response = requests.get(NEWS_ENDPOINT, params=news_params)
	articles = news_response.json()['articles']
	three_article = articles[:3]
	# print(three_articles)

	formatted_articles = [f"Headline:{article['title']}. \nBrief: {article ['description']}" for article in three_article]

	client = Client(account_sid, auth_token)

	for article in formatted_articles:
		message = client.messages \
		                .create(
		                     body=f"{article}",
		                     from_='+19705368315',
		                     to='+916302396971'
		                 )
