import feedparser
import json
import urllib.request
import datetime

from urllib.parse import quote
from flask import Flask
from flask import render_template
from flask import request
from pprint import pprint
from flask import make_response


app = Flask(__name__)

RSS_FEEDS = {
    'bbc' : 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn' : 'http://rss.cnn.com/rss/edition.rss',
    'fox' : 'http://feeds.foxnews.com/foxnews/latest',
    'iol' : 'http://www.iol.co.za/cmlink/1.640'
}

DEFAULTS = {
    'publication' : 'cnn',
    'city' : 'Calcutta, IN',
    'currency_from' : 'USD',
    'currency_to' : 'INR'
}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=65b8831d1736fe05836815097ae4a457"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=09f8ae338add4275a341e3c556444eae"

@app.route("/")
def home():
    #publication = request.args.get("publication")
    #if not publication:
        #publication = request.cookies.get("publication")
        #if not publication:
            #publication = DEFAULTS['publication']
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    #city = request.args.get('city')
    #if not city:
        #city = DEFAULTS['city']
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    #currency_from = request.args.get("currency_from")
    #currency_to = request.args.get("currency_to")
    #if not currency_from:
        #currency_from = DEFAULTS['currency_from']
    #if not currency_to:
        #currency_to = DEFAULTS['currency_to']
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rates(currency_from, currency_to)

    response = make_response(
        render_template(
            "home.html",
            articles = articles,
            weather = weather,
            currency_from = currency_from,
            currency_to = currency_to,
            rate = rate,
            currencies = sorted(currencies),
            feeds = RSS_FEEDS,
            publication = publication,
            city = city
        )
    )
    expires = datetime.datetime.now() + datetime.timedelta(days = 365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    query = quote(query)
    url = WEATHER_URL.format(query)
    data = urllib.request.urlopen(url).read().decode("utf-8")
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {
            "description" : parsed["weather"][0]["description"],
            "temperature" : parsed["main"]["temp"],
            "city" : parsed["name"],
            "country" : parsed["sys"]["country"]
        }
    return weather

def get_rates(from_rate, to_rate):
    all_currency = urllib.request.urlopen(CURRENCY_URL).read().decode("utf-8")
    parsed = json.loads(all_currency).get('rates')
    parsed_from_rate = parsed.get(from_rate.upper())
    parsed_to_rate = parsed.get(to_rate.upper())
    return (parsed_to_rate/parsed_from_rate, parsed.keys())

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
#65b8831d1736fe05836815097ae4a457 #WEATHER_URL
#09f8ae338add4275a341e3c556444eae #CURRENCY_URL
