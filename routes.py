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
import nltk
from nltk.corpus import stopwords

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
    def stopwordss(wordscopy):
        for x in wordscopy:
            return [x for x in wordscopy if x not in stopwords.words('english')]
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
        
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)

        wordcloud.to_file("wordcloud.png")

        pl = TextBlob(text).sentiment.polarity
        su = TextBlob(text).sentiment.subjectivity
        # if pl <= 0:
        #     status = 'Negative'
        # else:
        #     status = 'Positive'

        # sentences = text.split(".")
        # sumsen = 0
        # tns = 0
        # for y in sentences:
        #     tns = tns + 1  # Total Number of Sentences

        # words = text.split(" ")
        # tnw = 0
        # wordscopy = words

        # wordscopy = stopwordss(wordscopy)

        # punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        # wordscopy2 = ""
        # for char in wordscopy:
        #     if char not in punctuations:
        #         wordscopy2 = wordscopy2 + char

        # for x in wordscopy:
        #     tnw = tnw + 1  # Total number of words

        # ccw = 0
        # cwp = ['un', 'non', 'in', 'pre', 'trans', 're', 'con']
        # cws = ['ly', 'ist', 'er', 'ness', 'ment', 's', 'ing', 'ed', 'en', 'est', 'mit', 'ceive', 'fer']
        # for y in words:
        #     for y2 in cwp:
        #         if y.startswith(y2):
        #             ccw = ccw + 1
        #     for y2 in cws:
        #         if y.endswith(y2):
        #             ccw = ccw + 1

        # pcw = ccw / tnw

        # fi = 0.4 * ((tnw / tns) + 100 * (ccw / tnw))

        # anws = tnw / tns

        # sc = 0
        # for w in wordscopy2:
        #     if (
        #             w == 'a' or w == 'e' or w == 'i' or w == 'o' or w == 'u' or w == 'A' or w == 'E' or w == 'I' or w == 'O' or w == 'U'):
        #         sc = sc + 1

        # scw = sc / tnw

        # pronounRegex = re.compile(
        #     r'\b(I|me|mine|myself|us|our|ourselves|you|your|yours|yourself|yourselves|he|him|himself|his|she|her|hers|herself|it|its|itself|they|them|their|theirs|themselves|we|my|ours|(?-i:us))\b',
        #     re.I)
        # pronouns = pronounRegex.findall(text)

        # asl = len(wordscopy2) / tns
        # awl = len(wordscopy2) / tnw

        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'wordcloud.png')

        # return render_template('index.html',form=form,hashtag=form.hashtag.data,text=text,Sub=su,Pol=pl,loc=full_filename,status=status,tns=tns,tnw=tnw,ccw=ccw,pcw=pcw,fi=fi,anws=anws,sc=sc,scw=scw,pronouns=len(pronouns),asl=asl,awl=awl)
        return render_template('index.html',form=form,hashtag=form.hashtag.data,text=text,Sub=su,Pol=pl,loc=full_filename)

    return render_template('index.html',form=form,hashtag=form.hashtag.data)

