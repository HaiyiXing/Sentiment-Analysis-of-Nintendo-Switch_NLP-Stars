#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 18:30:57 2020

@author: jordanlui
"""
#Merge the amazon and walmart csv file into a dataframe 
import pandas as pd
# df1 = pd.read_csv("/Users/jordanlui/Desktop/walmart.csv")
# df2 = pd.read_csv("/Users/jordanlui/Desktop/amazon.csv")

# df1.rename(columns={'Rate':"Rating"},inplace=True)
# df2.drop(['title'],axis=1, inplace=True)
# df2.columns = ['Rating','Date','Content']
# df = pd.concat([df1,df2],sort=False)
# df['Date'] =pd.to_datetime(df.Date)
# df.sort_values(by=['Date'],inplace=True)

df.to_csv("/Users/jordanlui/Desktop/review.csv",index=False)

df = pd.read_csv("/Users/jordanlui/Desktop/review.csv")

#Preprocess data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stopwords_list = stopwords.words('english')

def Data_cleaning(contents):
    tokens = [w for w in word_tokenize(contents.lower()) if w.isalpha()]
    no_stops = [t for t in tokens if t not in stopwords_list]
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in no_stops]
    return lemmatized

#Return a list of filtered words in each review
df['Words'] = df['Content'].apply(Data_cleaning)

#Creat a bag of words
def BOW(tokens):
    return dict([[tk, tokens.count(tk)] for tk in set(tokens)])

df['BOW'] = df['Words'].apply(BOW)

#Create a Wordcloud

from wordcloud import WordCloud
import matplotlib.pyplot as plt

#Add unmeaningful words to the stopwords list
stopwords_list.extend(['game','switch','nintendo','one','really',
                       'would','buy','bought','came','get','got',
                       'still','son','kid'])
comment_words = ''
for wordlist in df['Words']:
    for word in wordlist:
        comment_words = comment_words + word + ' '
                         
wordcloud = WordCloud(stopwords=stopwords_list,
            background_color='white').generate(comment_words)    

plt.imshow(wordcloud,interpolation='bilinear') 
plt.axis('off')
plt.show()

#Get sentiment score          
from textblob import TextBlob

def Get_sentiment_score(contents):
    return TextBlob(contents).sentiment.polarity

df['Sentiment Score'] = df['Content'].apply(Get_sentiment_score)

df = df[df['Sentiment Score']!=0]

# df.to_csv("/Users/jordanlui/Desktop/review_new.csv",index=False)



