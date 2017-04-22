import feedparser
from random import randint
from flask import Flask

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
    random_article_no = randint(0, len(feed['entries']))
    first_article = feed['entries'][random_article_no]
    return """
        <html>
            <head>
                <title>Headlines ({3})</title>
            </head>
            <body>
                <h1>Headlines ({3})</h1>
                <b>{0}</b> <br />
                <i>{1}</i> <br />
                <p>{2}</p> <br />
            </body>
        </html>
    """.format(
            first_article.get("title"),
            first_article.get("published"),
            first_article.get("summary"),
            publication
        )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
