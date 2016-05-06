import feedparser

from flask import Flask

from flask import render_template

app = Flask(__name__)

RSS_FEEDS = {'qdance': 'http://podcast.q-dance.nl/audio/q-dancepodcast.xml',
			 'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
			 'cnn': 'http://rss.cnn.com/rss/edition.rss',
			 'fox': 'http://feeds.foxnews.com/foxnews/latest'}

@app.route("/")
@app.route("/<publication>")

def get_news(publication='qdance'):
	feed = feedparser.parse(RSS_FEEDS[publication])
	first_article = feed['entries'] [0]
	return render_template("home.html", articles=feed['entries'])

if __name__ == '__main__':
	app.run(port=5000, debug=True)