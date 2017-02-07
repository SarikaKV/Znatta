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
import numpy as np

def remove_stop_words(sentence):
    stop = stopwords.words('english')
    return [i for i in sentence.lower().split() if i not in stop]
def read_df_from_csv(file_path): 
    return pd.DataFrame.from_csv(file_path)
def pos_tagging(sentence,is_adjective): 
    adjectives = []
    nouns = []
    i = 0
    result = [] 
    #i = i + 1
    #print i
    #Remove stop words if needed
    #text = remove_stop_words(sentence)
    #Stemming also can be done
    text=nltk.word_tokenize(sentence)
    tagged_words = nltk.pos_tag(text)
    for word in tagged_words:
            if(is_adjective is None):
                if (word[1] == 'JJ'):
                    adjectives.append(word[0])
                    #print word[0]
            else:
                if ((word[1] == 'NN') | (word[1] == 'NG')):
                    nouns.append(word[0])
                    #print word[0]
    if(is_adjective is  None):
        result = adjectives
    else:
        result = nouns
    return result

if __name__ == "__main__":
    feature_set = ['sound ','headphones','kross','quality','PortaPro',' phones','sound,']
    df = read_df_from_csv('C:/Hackthon/Znatta/all_sentence_df.csv')
    #Cleansing data
    df = df[df['sentences'] != '"']
    df = df[df['sentences'] != ' ']
    df['sentences'].replace('', np.nan, inplace=True)
    df.dropna(subset=['sentences'], inplace=True)
    
    #make new dataframe with new columns
    all_reviewerID =[]
    all_sentences = []
    all_features =[]
    all_opinion_words =[]
    all_senti_oreintation = []
    for review_sent in df[['reviewerID','sentences']].iterrows():
        reviewer = review_sent[1][0]
        sentence =review_sent[1][1]
        sentence = sentence.lower()
        for feature in feature_set:
            feature = feature.lower()
            all_reviewerID.append(reviewer)
            all_sentences.append(sentence)
            if(sentence.find(feature) != -1):
            #if(feature in sentence):
#                 if((feature == 'kross') | (feature == 'PortaPro') | (feature == 'phones') ):
#                     feature = 'headphones'
                all_features.append(feature)
                #all_opinion_words.append(pos_tagging(sentence,None))
            else:
                all_features.append('')
                #all_opinion_words.append('')
    df_new = DataFrame({'reviewerID' : all_reviewerID, 'sentences': all_sentences,'features' : all_features})
    df_new = df_new[df_new['features'] != '']
    df_new.to_csv('C:/Hackthon/Znatta/all_sentences_features_df.csv',sep = ',')
    print len(df_new)