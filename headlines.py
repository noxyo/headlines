
import feedparser

import json
import urllib2
import urllib

from flask import Flask

from flask import render_template

from flask import request

app = Flask(__name__)


WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=e950e0ad047e4aeb3d44f682902483ae"

RSS_FEEDS = {'qdance': 'http://podcast.q-dance.nl/audio/q-dancepodcast.xml',
			 'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
			 'cnn': 'http://rss.cnn.com/rss/edition.rss',
			 'fox': 'http://feeds.foxnews.com/foxnews/latest'}

DEFAULTS = {'publication': 'qdance',
			'city': 'Braga,PT'}


@app.route("/")


def home():
	# get customized headlines, based on user input or default
	publication = request.args.get('publication')
	if not publication:
		publication = DEFAULTS['publication']
	articles = get_news(publication)
	# get customized weather based on user input or default
	city = request.args.get('city')
	if not city:
		city = DEFAULTS['city']
	weather = get_weather(city)
	return render_template("home.html", articles=articles,weather=weather)

def get_news(query):
	if not query or query.lower() not in RSS_FEEDS:
		publication = DEFAULTS["publication"]
	else:
		publication = query.lower()
	feed = feedparser.parse(RSS_FEEDS[publication])
	return feed['entries']

def get_weather(query):
	#api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=e950e0ad047e4aeb3d44f682902483ae"
	query = urllib.quote(query)
	url = WEATHER_URL.format(query)
	data = urllib2.urlopen(url).read()
	parsed = json.loads(data)
	weather = None
	if parsed.get("weather"):
		weather = { "description": parsed["weather"][0]["description"],
					"icon": parsed["weather"][0]["icon"],
					"temperature": parsed["main"]["temp"],
					"city": parsed["name"],
					'country': parsed['sys']['country']
				  }
	return weather	

if __name__ == '__main__':
	app.run(port=5000, debug=True)