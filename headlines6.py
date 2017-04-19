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

@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("London, UK")
    return render_template("home2.html", articles=feed['entries'], feeds=RSS_FEEDS, publication = publication, weather=weather)

def get_weather(query):
    #api_url = http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=65b8831d1736fe05836815097ae4a457
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=65b8831d1736fe05836815097ae4a457"
    query = quote(query)
    url = api_url.format(query)
    print(url)
    data = urllib.request.urlopen(url).read().decode("utf-8")
    print(type(data))
    parsed = json.loads(data)
    print(type(parsed))
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
