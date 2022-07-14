from email import message
import os
from pydoc import cli
from numpy import diff
import requests
from twilio.rest import Client


phone_no = input("enter your phone number")


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

# Alpha Vantage API
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "ZZH3DTN0JDE637DG"

# News API
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "f4d2bced11474f1eb5d0feb0f8cbc9c3"

# Stock Details
STOCK_NAME = "TWTR"
COMPANY = "Twitter Inc."

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
# print(response.json())
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]


day_before_yestertday_data = data_list[1]
day_before_yestertday_closing_price = day_before_yestertday_data["4. close"]

difference = abs(float(yesterday_closing_price) -
                 float(day_before_yestertday_closing_price))
diff_percent = (difference / float(yesterday_closing_price)) * 100


news_params = {
    "apiKey": NEWS_API_KEY,
    "qInTitle": COMPANY,
}

if diff_percent > 3:
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    top_articles = articles[:3]

    formatted_articles = [
        f"Headline : {article['title']}. \n Desc : {article['description']}." for article in top_articles]

    client = Client(account_sid, auth_token)
    for new_article in formatted_articles:
        message = client.messages.create(
            body=new_article,
            from_="+19705368315",
            to=f"{phone_no}",
        )