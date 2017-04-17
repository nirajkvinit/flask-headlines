import feedparser
from random import randint
from flask import Flask
from flask import render_template

app = Flask(__name__)

RSS_FEEDS = {
    'bbc' : 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn' : 'http://rss.cnn.com/rss/edition.rss',
    'fox' : 'http://feeds.foxnews.com/foxnews/latest',
    'iol' : 'http://www.iol.co.za/cmlink/1.640'
}

@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    #random_article_no = randint(0, len(feed['entries']))
    #first_article = feed['entries'][random_article_no]
    #return render_template("home.html", title=first_article.get('title'), published=first_article.get('published'), summary=first_article.get('summary'))
    #return render_template("home.html", article = first_article)
    return render_template("home.html", articles=feed['entries'])

if __name__ == "__main__":
    app.run(port=5000, debug=True)
