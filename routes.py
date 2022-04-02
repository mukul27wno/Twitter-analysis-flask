from app import app 
from flask import render_template
import tweepy 
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import os
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
    # print("Submitted title 1 ",form.hashtag.data)
    if form.validate_on_submit():
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'wordcloud.png')
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
        
        text = re.sub('@[A-Za-z0-9]+','',text)  #remove @mentions
        text = re.sub(r'#', '',text)    #remove the '#' symbol
        text = re.sub(r'RT[\s]','',text)    #remove RT
        text = re.sub(r'https?:\/\/\S+','',text)    #remove link
        
        Sub = TextBlob(text).sentiment.subjectivity
        Pol = TextBlob(text).sentiment.polarity
        
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)

        wordcloud.to_file("wordcloud.png")

        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'wordcloud.png')

        return render_template('index.html',form=form,hashtag=form.hashtag.data,text=text,Sub=Sub,Pol=Pol,loc=full_filename)

    return render_template('index.html',form=form,hashtag=form.hashtag.data)

