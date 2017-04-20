import feedparser
import json
import urllib.request

from urllib.parse import quote
from flask import Flask
from flask import render_template
from flask import request
from pprint import pprint


app = Flask(__name__)

RSS_FEEDS = {
    'bbc' : 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn' : 'http://rss.cnn.com/rss/edition.rss',
    'fox' : 'http://feeds.foxnews.com/foxnews/latest',
    'iol' : 'http://www.iol.co.za/cmlink/1.640'
}

DEFAULTS = {
    'publication' : 'cnn',
    'city' : 'Calcutta, IN'
}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=65b8831d1736fe05836815097ae4a457"

@app.route("/")
def home():

    publication = request.args.get("publication")
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)

    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)

    return render_template("home2.html", articles = articles, weather = weather, feeds = RSS_FEEDS, publication = publication, city = city)

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
    print(url)
    data = urllib.request.urlopen(url).read().decode("utf-8")
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {
            "description" : parsed["weather"][0]["description"],
            "temperature" : parsed["main"]["temp"],
            "city" : parsed["name"]
        }
    return weather

if __name__ == "__main__":
    app.run(port=5000, debug=True)
#http://api.openweathermap.org/data/2.5/weather?q=London%2C%20UK&units=metric&appid=65b8831d1736fe05836815097ae4a457
