from app import app 
from flask import render_template
import tweepy 
# from textblob import TextBlob
# from wordcloud import WordCloud
import pandas as pd
# import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

import forms

@app.route('/',methods=['GET','POST'])
@app.route('/index.html', methods=['GET','POST'])
def index():

    log = pd.read_excel("login_twitter_api.xlsx")
    key = log['address']
    ckey = key[0]
    cskey = key[1]
    at = key[2]
    ats = key[3]

    form = forms.AddTaskForm()
    print("Submitted title 1 ",form.hashtag.data)
    # if form.validate_on_submit():
    #     print("Submitted title",form.hashtag.data)
    #     return render_template('result.html', form=form, hashtag=form.hashtag.data)
    if form.validate_on_submit():
        auth = tweepy.OAuthHandler(ckey, cskey)
        auth.set_access_token(at, ats)
        api = tweepy.API(auth, wait_on_rate_limit = True)
        hashtag = form.hashtag.data
        noft = form.noft.data
        lang = form.lng.data
        text = ''
        for q in hashtag:
            for tweets in api.search_tweets(q=q,lang=lang,count=noft):
                text = text + tweets.text
        return render_template('index.html',form=form,hashtag=form.hashtag.data,text=text)

         

    return render_template('index.html',form=form,hashtag=form.hashtag.data)

