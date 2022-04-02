# from one python file to another python file we can use import function
# take input from html page and use it into python file
# after using python input we have to show it to html page
import tweepy 
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

log = pd.read_csv("login.csv")
ckey = log['key'][0]
cskey = log['key'][1]
at = log['key'][2]
ats = log['key'][3]

forms = forms.AddTaskForm()

auth = tweepy.OAuthHandler(ckey, cskey)
auth.set_access_token(at, ats)
api = tweepy.API(authenticate, wait_on_rate_limit = True)
hashtag = forms.hashtag.data
noft = forms.noft.data
lang = forms.lng.data
# qurey = 'Mukul Goyal search'
posts = api.user_timeline(screen_name=hashtag, count=noft, lang=lang, tweet_mode='extended')
# posts = api.search_tweets(q=qurey,lang=lang,count=noft)
# i = 1
# print("Show the 5 recent tweets: \n")
# for tweet in posts[0:5]:
#     print(str(i) +') '+ tweet.full_text + '\n')
#     i = i+1

# df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
# df.head()

# in search query we can add state name as well for the specified state result
# add all tweet text do text cleaning polarity wordCloud Subjectivity 


def cleantxt(text):
    return text 

df['Tweets']=df['Tweets'].apply(cleantxt)

def getsub(text):
    return TextBlob(text).sentiment.subjectivity

def getpol(text):
    return TextBlob(text).sentiment.polarity

df['Subjectivity'] = df['Tweets'].apply(getsub)
df['Polarity'] = df['Tweets'].apply(getpol)

# df
allwords = " ".join([twts for in df['Tweets']])
wordCloud = WordCloud(width = 500, height=300, random_state = 21, max_font_size = 119).genrate(allwords)

# plt.imshow(wordCloud, interpolation = 'bilinear')
# plt.axis('off')
# plt.show()
def getAnalysis(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Netural"
    else:
        return "Positive"

df['Analysis'] = df['Polarity'].apply(getAnalysis)
j=1
sortedDF = df.sort_values(by=['Polarity'])
for i in range(0, sortedDF.shape[0]):
    # print(str(j)+') '+sortedDF['Tweets'][i])
    j = j+1

j=1
sortedDF = df.sort_values(by=['Polarity'], ascending='False') 
for i in range(0,sortedDF.shape[0]):
    if(sortedDF['Analysis'][i]=='Negative'):
        # print(sortedDF['Tweets'][i])
        j = j+1

plt.figure(figsize=(8,6))
for i in range(0, df.shape[0]):
    # plt.scatter(df['Polarity'][i], df['Subjectivity'], color='Blue')

# plt.title('Sentiment Analysis')
# plt.xlabel('Polarity')
# plt.ylabel('Subjectivity')
# plt.show()

ptweets = df[df.Analysis == 'Postive']
ptweets = ptweets['Tweets']
round((ptweets.shape[0]/df.shape[0])*100,1)

ntweets = df[df.Analysis == 'Negative']
ntweets = ntweets['Tweets']

round( (ntweets.shape[0]/df.shape[0]*100),1)

df['Analysis'].value_counts()

# plt.title("Sentiment Analysis")
# plt.xlabel("Sentiment")
# plt.ylabel("Counts")
# df['Analysis'].value_counts().plot(kind='bar')
# plt.show() 