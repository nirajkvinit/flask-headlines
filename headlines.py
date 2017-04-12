import feedparser
from random import randint
from flask import Flask

app = Flask(__name__)

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"
#http://www.novamining.com/feed/

@app.route("/")
def get_news():
    feed = feedparser.parse(BBC_FEED)
    #print('total length: ', len(feed['entries']))
    random_article_no = randint(0, len(feed['entries']))
    first_article = feed['entries'][random_article_no]
    return """<html>
        <body>
            <h1>BBC Headlines</h1>
            <b>{3}. {0}</b><br/>
            <i>{1}</i><br/>
            <p>{2}</p>
        </body>
    </html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"), random_article_no)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
