import json
import gzip
import re 
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np

def remove_stop_words(sentence):
    stop = stopwords.words('english')
    return [i for i in sentence.lower().split() if i not in stop]
def read_df_from_csv(file_path): 
    return pd.DataFrame.from_csv(file_path)
def get_sentiment(opinion):
    seed_list = {"good": 1, "excellent": 1,"cool":1, "nice": 1,"fabulous":1,"fantastic":1,"supreme":1,"durable":1,
                 "important":1,"reliable": 1,"amazing":1, "great":  1,"beautiful":1,"comfortable":1,"phenomenal":1,
                 "perfect":1,"happy":1,"superb":1,"pretty":1,"portable" :1,"fine":1,"recommended":1,"unbelievable":1,
                 "stylish":1,"clear":1,"unique":1,"cheap":1,"exceptional":1,"impressive":1,"impressed":1,"suitable":1,
                 "rich":1,"reasonable":1,"remarkable": 1,"smooth":1,"soft":1,"worth":1,
                 "uncomfortable": 2,"frustrating":2,"crappy":2, "not" : 2,"cant":2,"bad":2,"unreliable":2,"poor":2,"ugly":2,
                 "worst":2,"wrong":2,"distorted":2,"expensive":2,"exaggerated":2,"low":2, "sad":2,"hard":2,"disappointed":2}
    sentiment = 0
    
    if opinion in seed_list:
        sentiment = seed_list[opinion]
        print opinion
    else:
        syns = wordnet.synsets(opinion)
        print opinion,':',syns
        for syn in syns:
            for l in syn.lemmas():
                print 'l = ', l.name()
                if l.name() in seed_list:
                   sentiment = seed_list[l.name()]
                   seed_list[opinion] = sentiment 
            
    print 'sentiment',sentiment            
    return sentiment       
            
if __name__ == "__main__":
    
    df = read_df_from_csv('C:/Hackthon/Znatta/all_sentences_features_opinions_df.csv')
    #Cleansing data
    print len(df)
    df = df.drop_duplicates()
    print len(df)
    i = 0
    #make new dataframe with new columns
    all_reviewerID =[]
    all_sentences = []
    all_features =[]
    all_opinion_words =[]
    all_senti_oreintation = []
    for review_sent in df[['reviewerID','sentences','features','opinion']].iterrows():
        if (i <2):
            i = i+1
            print i
            reviewer = review_sent[1][0]
            all_reviewerID.append(reviewer)
            sentence =review_sent[1][1]
            all_sentences.append(sentence)
            feature = review_sent[1][2]
            all_features.append(feature)
            opinion = review_sent[1][3]
            all_opinion_words.append(opinion)
            sentiment = get_sentiment(opinion)
            all_senti_oreintation.append(sentiment)
            
    print len(all_sentences),len(all_opinion_words)  , len(all_features)         
    df_new = DataFrame({'reviewerID' : all_reviewerID, 'sentences': all_sentences,'features' : all_features,'opinion':all_opinion_words,'sentiment':all_senti_oreintation})
    
    df_new.to_csv('C:/Hackthon/Znatta/all_sentences_features_opinions_sentiment_df.csv',sep = ',')
    print len(df_new)