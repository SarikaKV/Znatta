
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


def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield json.dumps(eval(l))

def getDF(path):
  i = 0
  reviewerID = []
  asin = []
  reviewerName = []
  unixReviewTime = []
  reviewText = []
  overall = []
  summary = []
  for d in parse(path):
    #if(i < 2):
    #B00001P4ZH: Koss PortaPro Headphones with Case
    if(d.find('B00001P4ZH') != -1):
        s = d.split(':')
        #print d
        reviewerID.append(s[1].split(',')[0])
        if(d.find('"asin":') != -1):
            a= s[2].split(',')[0]
            asin.append(str.replace(str(a),'"',""))
        else:
            asin.append('')
        reviewerName.append(s[3].split(',')[0])
        unixReviewTime.append(s[5].split(',')[0])
        if(d.find('"reviewText":') != -1):
            if(d.find('"overall"') != -1):
                reviewText.append(str.replace(d[d.index('"reviewText":') : -(len(d) - d.index(', "overall"') )],'"reviewText": ',''))
            elif(d.find('"reviewTime"') != -1):
                reviewText.append(str.replace( d[d.index('"reviewText":') : -(len(d) - d.index(', "reviewTime"') )],'"reviewText": ',''))
            elif(d.find('"summary"') != -1):
                reviewText.append(str.replace( d[d.index('"reviewText":') : -(len(d) - d.index(', "summary"') )],'"reviewText": ',''))
        if(d.find('"overall":') != -1):  
            if(d.find('"reviewTime"') != -1):      
                overall.append( d[d.index('"overall":') : -(len(d) - d.index(', "reviewTime"') )])
            elif(d.find('"summary"') != -1):      
                overall.append( d[d.index('"overall":') : -(len(d) - d.index(', "summary"') )])
            else:
              overall.append( d[d.index('"overall":') : -(len(d) - d.index('}') )])  
        else:
            overall.append('')
        if(d.find('"summary":') != -1):
            sum = str.replace(str.replace(d[d.index('"summary":') : -(len(d) - d.index('}') )],'"summary": ',''),'"','')
            #print sum
            summary.append(sum )
        else:
            summary.append('')
        i += 1
  #print asin
  df = DataFrame({'reviewerID' : reviewerID, 'asin': asin,'reviewerName' : reviewerName, 'unixReviewTime': unixReviewTime, 'reviewText' : reviewText, 'overall': overall,'summary' : summary})
  #return pd.DataFrame.from_dict(df, orient='index')
  return d
def plot_word_cloud(terms):   
    wc = WordCloud(height=1000, width=1000, max_words=1000).generate(" ".join(terms))
    
    plt.figure(figsize=(10, 10))
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    
def model_build_and_plot(reviews):
    vec = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_df=.5)
    tfv = vec.fit_transform(reviews)
    terms = vec.get_feature_names()
    plot_word_cloud(terms)
def remove_stop_words(sentence):
    stop = stopwords.words('english')
    return [i for i in sentence.lower().split() if i not in stop]
def read_df_from_csv(file_path): 
    return pd.DataFrame.from_csv(file_path)
def pos_tagging(reviews,is_adjective): 
    adjectives = []
    nouns = []
    i = 0
    result = []
    for review in reviews: 
        #i = i + 1
        #print i
        #Remove stop words if needed
        #text = remove_stop_words(sentence)
        #Stemming also can be done
        text=nltk.word_tokenize(review)
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
    #UnComment this when the product is changed
    #df = getDF("C:/Users/310106108/Downloads/reviews_Electronics_5.json.gz")
    #df.to_csv('C:/Hackthon/Znatta/input_df.csv',sep = ',')
    df = read_df_from_csv('C:/Hackthon/Znatta/input_df.csv')
    sound_review = []
    headphones_review = []
    price_review = []
    quality_review =[]
    look_review = []
    all_review_features = []
    print len(df)
    i = 0
    reviewerID_all = []
    sentences_all = []
    for review in df[['reviewerID','reviewText']].iterrows():
        reviewer = review[1][0]
        print review[1][1]
        sentences = []
        sentences = review[1][1].split('.')
        
        for sentence in sentences:
            sentences_all.append(sentence)
            reviewerID_all.append(reviewer)
        #Feature Identification can be done to programatically determine the most talked about features
        #features = pos_tagging(sentences, 'no')
        #all_review_features.append(features)
        #Manual Feature extraction
        #=======================================================================
        # for sentence in sentences:
        #     sentence = sentence.replace('"','')            
        #     if(sentence.find('sound') != -1):
        #         sound_review.append(sentence)
        #     if(sentence.find('headphones') != -1):
        #         headphones_review.append(sentence)
        #     if(sentence.find('price') != -1):
        #         price_review.append(sentence)
        #     if(sentence.find('quality') != -1):
        #         quality_review.append(sentence)
        #     if(sentence.find('look') != -1):
        #         look_review.append(sentence)
        #=======================================================================
        i = i+1
        print i
    df_all_sentences = DataFrame({'reviewerID' : reviewerID_all, 'sentences' : sentences_all})
    df_all_sentences.to_csv('C:/Hackthon/Znatta/all_sentence_df.csv',sep = ',')
    all_summary = [t for t in df.summary]
     #Feature Identification can be done to programatically determine the most talked about features
    df_nouns = DataFrame({'features' : all_review_features})
    df_nouns['feature_count']  = 1
    df_grouped = df_nouns.groupby(['features']).count()
    df_grouped = df_grouped.reset_index()
    features_ordered = df_grouped.sort('features',ascending = False)
    print    features_ordered
    
    #Build models and plot word cloud
    #===========================================================================
    # model_build_and_plot(all_summary)
    # 
    # model_build_and_plot(sound_review)
    # model_build_and_plot(headphones_review)
    # model_build_and_plot(price_review)
    # model_build_and_plot(quality_review)
    # model_build_and_plot(look_review)
    #===========================================================================
    
    #POS Tagging at feature level
    print len(sound_review)
    sound_adjectives = pos_tagging(sound_review,None)
    model_build_and_plot(sound_adjectives)