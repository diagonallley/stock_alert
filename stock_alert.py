import os
import requests
from twilio.rest import Client

STOCK = "TATASTEEL.BSE"
COMPANY_NAME = "TATA STEEL"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_KEY = ""
NEWSAPI_KEY = ""

data = requests.get(STOCK_ENDPOINT, params={
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": STOCK_KEY
})

data.raise_for_status()

list_of_stockdata = [v for k, v in data.json()["Time Series (Daily)"].items()]

yest_data = list_of_stockdata[0]
yest_closing_price = yest_data["4. close"]


day_before_yest_data = list_of_stockdata[1]
day_before_yest_closing_price = day_before_yest_data["4. close"]


difference = (float(yest_closing_price) -
              float(day_before_yest_closing_price))
up_down = None
if difference > 0:
    up_down = "⬆️📈"
else:
    up_down = "⬇️📉"
print(difference)

percentage_difference = round(
    (difference/float(yest_closing_price))*100, 2)
print(percentage_difference)

if abs(percentage_difference) > 1:
    print("Get News")

    data = requests.get(NEWS_ENDPOINT, params={
        "apiKey": NEWSAPI_KEY,
        # "language": "English",
        "qInTitle": COMPANY_NAME
    })

    posts = data.json()["articles"]
    articles = posts[0:3]

    ret_arr = [f"{item['title']}:{item['description']}" for item in articles]
    print(ret_arr)

    account_sid = ""
    auth_token = os.environ.get("TWILIO_TOKEN")
    client = Client(account_sid, auth_token)
    for article in ret_arr:
        message = client.messages.create(
            to="+", from_="+", body=f"The stock went {abs(difference)} % {up_down}\n{article}")

