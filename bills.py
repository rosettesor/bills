import os
import model
import tweepy
import itertools
import unicodedata
from datetime import datetime, timedelta
from time import sleep
from flask import Flask, render_template, redirect, session, url_for, request


app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/", methods = ['GET', 'POST'])
def index():
	api = tweepy.API()

	# to avoid duplication of tweets in database
	in_db = model.session.query(model.Tweet).filter(model.Tweet.id_num).all()
	in_db_list = []
	for twit in in_db: 
		twit_id = twit.id_num
		in_db_list.append(twit_id)

	for tweet in tweepy.Cursor(api.search, q="bills.com", rpp=20,\
		result_type="recent", include_entities=True, lang="en").items(20):
		if tweet.id not in in_db_list:
			new_tweet = model.Tweet()
			new_tweet.username = tweet.from_user
			new_tweet.user_image = tweet.profile_image_url
			new_tweet.text = tweet.text
			new_tweet.id_num = tweet.id
			new_tweet.date = tweet.created_at
			new_tweet.read = "N"
			model.session.add(new_tweet)
			model.session.commit()

	top_10 = model.session.query(model.Tweet).order_by(model.Tweet.date.desc()).all()
	top_10_list = itertools.islice(top_10, 0, 10)

	# for tweet in top_10_list:
	# 	checked = request.form["read"]
	# 	print checked
	# 	# if tweet.read == "N":

	return render_template("index.html", list_10 = top_10_list)

if __name__ == "__main__":
	app.run(debug = True)