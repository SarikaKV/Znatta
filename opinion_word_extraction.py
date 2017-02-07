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
    feature_set = ['sound','headphones','kross','quality','PortaPro','phones']
    df = read_df_from_csv('C:/Hackthon/Znatta/all_sentences_features_df.csv')
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
    for review_sent in df[['reviewerID','sentences','features']].iterrows():
        #if (i <20):
            i = i+1
            print i
            reviewer = review_sent[1][0]
            all_reviewerID.append(reviewer)
            sentence =review_sent[1][1]
            all_sentences.append(sentence)
            feature = review_sent[1][2]
            all_features.append(feature)
            opinion_words = pos_tagging(sentence,None)
            opinion_word = ''
            if(len(opinion_words) > 1):
                last_opinion_word = opinion_words[len(opinion_words) - 1]
                
                if(sentence.index(feature) > sentence.index(last_opinion_word)):
                    opinion_word = ''
                else :
                    for opinion in opinion_words:
                        if(sentence.index(opinion) > sentence.index(feature)):
                           opinion_word = opinion
                           break
                        
            elif(len(opinion_words) == 1):
                opinion_word = opinion_words[0]   
            else:
                opinion_word = ''
            all_opinion_words.append(opinion_word)
    print len(all_sentences),len(all_opinion_words)  , len(all_features)         
    df_new = DataFrame({'reviewerID' : all_reviewerID, 'sentences': all_sentences,'features' : all_features,'opinion':all_opinion_words})
    df_new = df_new[df_new['opinion'] != '']
    df_new.to_csv('C:/Hackthon/Znatta/all_sentences_features_opinions_df.csv',sep = ',')
    print len(df_new)