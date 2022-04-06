from app import app 
from flask import render_template
import tweepy 
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import re
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
    
    # print("Submitted title 1 ",form.hashtag.data)
    if form.validate_on_submit():
        
        def removes(wordscopy):
            stopwords_hi = ['तुम','मेरी','मुझे','क्योंकि','हम','प्रति','अबकी','आगे','माननीय','शहर','बताएं','कौनसी','क्लिक','किसकी','बड़े','मैं','and','रही','आज','लें','आपके','मिलकर','सब','मेरे','जी','श्री','वैसा','आपका','अंदर', 'अत', 'अपना', 'अपनी', 'अपने', 'अभी', 'आदि', 'आप', 'इत्यादि', 'इन', 'इनका', 'इन्हीं', 'इन्हें', 'इन्हों', 'इस', 'इसका', 'इसकी', 'इसके', 'इसमें', 'इसी', 'इसे', 'उन', 'उनका', 'उनकी', 'उनके', 'उनको', 'उन्हीं', 'उन्हें', 'उन्हों', 'उस', 'उसके', 'उसी', 'उसे', 'एक', 'एवं', 'एस', 'ऐसे', 'और', 'कई', 'कर','करता', 'करते', 'करना', 'करने', 'करें', 'कहते', 'कहा', 'का', 'काफ़ी', 'कि', 'कितना', 'किन्हें', 'किन्हों', 'किया', 'किर', 'किस', 'किसी', 'किसे', 'की', 'कुछ', 'कुल', 'के', 'को', 'कोई', 'कौन', 'कौनसा', 'गया', 'घर', 'जब', 'जहाँ', 'जा', 'जितना', 'जिन', 'जिन्हें', 'जिन्हों', 'जिस', 'जिसे', 'जीधर', 'जैसा', 'जैसे', 'जो', 'तक', 'तब', 'तरह', 'तिन', 'तिन्हें', 'तिन्हों', 'तिस', 'तिसे', 'तो', 'था', 'थी', 'थे', 'दबारा', 'दिया', 'दुसरा', 'दूसरे', 'दो', 'द्वारा', 'न', 'नहीं', 'ना', 'निहायत', 'नीचे', 'ने', 'पर', 'पर', 'पहले', 'पूरा', 'पे', 'फिर', 'बनी', 'बही', 'बहुत', 'बाद', 'बाला', 'बिलकुल', 'भी', 'भीतर', 'मगर', 'मानो', 'मे', 'में', 'यदि', 'यह', 'यहाँ', 'यही', 'या', 'यिह', 'ये', 'रखें', 'रहा', 'रहे', 'ऱ्वासा', 'लिए', 'लिये', 'लेकिन', 'व', 'वर्ग', 'वह', 'वह', 'वहाँ', 'वहीं', 'वाले', 'वुह', 'वे', 'वग़ैरह', 'संग', 'सकता', 'सकते', 'सबसे', 'सभी', 'साथ', 'साबुत', 'साभ', 'सारा', 'से', 'सो', 'ही', 'हुआ', 'हुई', 'हुए', 'है', 'हैं', 'हो', 'होता', 'होती', 'होते', 'होना', 'होने', 'अपनि', 'जेसे', 'होति', 'सभि', 'तिंहों', 'इंहों', 'दवारा', 'इसि', 'किंहें', 'थि', 'उंहों', 'ओर', 'जिंहें', 'वहिं', 'अभि', 'बनि', 'हि', 'उंहिं', 'उंहें', 'हें', 'वगेरह', 'एसे', 'रवासा', 'कोन', 'निचे', 'काफि', 'उसि', 'पुरा', 'भितर', 'हे', 'बहि', 'वहां', 'कोइ', 'यहां', 'जिंहों', 'तिंहें', 'किसि', 'कइ', 'यहि', 'इंहिं', 'जिधर', 'इंहें', 'अदि', 'इतयादि', 'हुइ', 'कोनसा', 'इसकि', 'दुसरे', 'जहां', 'अप', 'किंहों', 'उनकि', 'भि', 'वरग', 'हुअ', 'जेसा', 'नहिं']
            stopwords_en = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
            to_be_removed = stopwords_hi + stopwords_en
            for x in wordscopy:
                return [x for x in wordscopy if x not in to_be_removed]

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
        emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', string=text)
        
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)

        wordcloud.to_file("wordcloud.png")

        pl = TextBlob(text).sentiment.polarity
        su = TextBlob(text).sentiment.subjectivity
        if pl <= 0:
            status = 'Negative'
        else:
            status = 'Positive'

        sentences = text.split(".")
        sumsen = 0
        tns = 0
        for y in sentences:
            tns = tns + 1  # Total Number of Sentences

        words = text.split(" ")
        tnw = 0
        wordscopy = words
        text = removes(text)
        # if form.lng.data == 'en':
        #     for x in wordscopy:
        #         return [x for x in wordscopy if x not in stopwords.words('english')]
        # if form.lng.data == 'hi':
        #     for x in wordscopy:
        #         return [x for x in wordscopy if x not in stopwords.indian.words('hindi.pos')]

        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        wordscopy2 = ""
        for char in wordscopy:
            if char not in punctuations:
                wordscopy2 = wordscopy2 + char

        for x in wordscopy:
            tnw = tnw + 1  # Total number of words

        ccw = 0
        cwp = ['un', 'non', 'in', 'pre', 'trans', 're', 'con']
        cws = ['ly', 'ist', 'er', 'ness', 'ment', 's', 'ing', 'ed', 'en', 'est', 'mit', 'ceive', 'fer']
        for y in words:
            for y2 in cwp:
                if y.startswith(y2):
                    ccw = ccw + 1
            for y2 in cws:
                if y.endswith(y2):
                    ccw = ccw + 1

        pcw = ccw / tnw

        fi = 0.4 * ((tnw / tns) + 100 * (ccw / tnw))

        anws = tnw / tns

        sc = 0
        for w in wordscopy2:
            if (
                    w == 'a' or w == 'e' or w == 'i' or w == 'o' or w == 'u' or w == 'A' or w == 'E' or w == 'I' or w == 'O' or w == 'U'):
                sc = sc + 1

        scw = sc / tnw

        pronounRegex = re.compile(
            r'\b(I|me|mine|myself|us|our|ourselves|you|your|yours|yourself|yourselves|he|him|himself|his|she|her|hers|herself|it|its|itself|they|them|their|theirs|themselves|we|my|ours|(?-i:us))\b',
            re.I)
        pronouns = pronounRegex.findall(text)

        asl = len(wordscopy2) / tns
        awl = len(wordscopy2) / tnw

        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'wordcloud.png')

        return render_template('index.html',form=form,hashtag=form.hashtag.data,text=text,Sub=su,Pol=pl,loc=full_filename,status=status,tns=tns,tnw=tnw,ccw=ccw,pcw=pcw,fi=fi,anws=anws,sc=sc,scw=scw,pronouns=len(pronouns),asl=asl,awl=awl)
        # return render_template('index.html',form=form,hashtag=form.hashtag.data,text=text,Sub=su,Pol=pl,loc=full_filename)

    return render_template('index.html',form=form,hashtag=form.hashtag.data)

