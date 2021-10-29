# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:31:10 2019

@author: seoleary
"""
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from pandas import DataFrame
import spacy
from spacy import displacy
from spacy.lang.en.stop_words import STOP_WORDS
import pickle
import os
import re



class collect_data(object):
    """
    Collects either training data, or validation data. 
    
    If training data is collected, lets the user identify which articles fall in the categories
        1 - Negative News
        0 - Not-Negative
        
    If validation data is collected, doesn't require input
    """
    
    def __init__(self):
        self.numResults, self.language = 60 , 'en'
        self.companies = self.get_companies()
        self.keywords = self.set_keywords()
        self.headline_dict = self.get_words(self.companies,self.keywords)
        self.Y = self.classify(self.headline_dict)
        #self.search_string = self.make_search_string(self.companies,self.keywords)
        #self.headlines, self.freq_dict = self.get_words(self.search_string, self.companies)
        #self.training_matrix = self.make_training_matrix(self.freq_dict.keys(),self.headlines)
        
        
    def get_companies(self, test_train = 'train'):
        x = []
        question = 'What company do you want to '+test_train+' with? '
        x.append(input(question))
        more = input('Another Company? (Y or N) ')
        while more == 'Y':
            company = input('Company name? ')
            x.append(company)  
            more = input('Another Company? (Y or N) ')            
            while more.lower() != 'Y' and more.lower()!= 'N':
                more = input('Another Company? (Y or N) ')                     
        return x
    
    def set_keywords(self):
        keywords = ['corruption','vulnerability','law suit','fines']
        for i in keywords[:]:
            print('Do you want the keyword',i,'? (Y or N) ')
            response = input()
            while response != 'Y' and response!= 'N':
                print('Please type Y or N ')
                response = input()
            if response == 'N':
                keywords.remove(i)
        other = input('Another keyword? (Y or N) ')
        while other != 'Y' and other != 'N':
            other = input('Please type Y or N ')
        while other == 'Y':
            other_name = input('Keyword to add? ')
            keywords.append(other_name)
            other = input('Another keyword? (Y or N) ')
            while other != 'Y' and other !='N':
                other = input('Please type Y or N ')
        return keywords
    
    def make_search_string(self,company,keyword):        
        search_string = '"'+company+'"+AND+"'+keyword+'"'
        return search_string
        
    def get_words(self,companies,keywords):
        search_strings = [self.make_search_string(x,y) for x in companies for y in keywords]
        headline_dict = {}
        for i in search_strings:
            googleUrl = 'https://www.google.com/search?q={}&num={}&hl={}&tbm=nws'.format(i, self.numResults, self.language)
            response = requests.get(googleUrl)
            response.raise_for_status()
            soup = BeautifulSoup(response.text,'lxml')
            headlines = soup.find_all('div', attrs={'class':'g'})
            for j in headlines:
                key = j.find('a',href=True)['href'][7:]
                if key not in headline_dict.keys() and j.text not in headline_dict.values():
                    headline_dict[key] = j.text.replace('\xa0',' ')
        #THE FOLLOWING FINDS THE URLS FOR THE HEADLINES
        #url =[x.find('a',href=True)['href'][7:] for x in headlines]
        return headline_dict
    
    def classify(self, headline_dict):
        Y = []
        print("Is this negative news? Type 'Y' for negative news and 'N' for non-negative news'\n'")
        for i in headline_dict.values():
            print(i)
            classified = str(input())
            while classified.lower()!='y' and classified.lower()!='n':
                print("PLEASE TYPE 'Y' OR 'N'")
            if classified.lower() == 'y':
                Y.append(1)
            else:
                Y.append(0)
        return Y

class process_data(object):
    
    def __init__(self):
        #self.nlp = spacy.load('en_core_web_lg')
        #for word in STOP_WORDS:
        #    self.nlp.vocab[word].is_stop =True
        pass
    
    def pre_process(self):
        pass
    
    def vectorize(self,headline_dict, tfidf = False, ngram = 1):
        #words = [self.process_words(x) for x in headline_dict.values()]
        words = headline_dict.values()
        if tfidf == True:
            vectorizer = TfidfVectorizer(stop_words = STOP_WORDS, ngram_range=(1,ngram))
        else:
            vectorizer = CountVectorizer(stop_words = STOP_WORDS, ngram_range=(1,ngram))
            
        trans = vectorizer.fit_transform(words)
        df = DataFrame(trans.toarray(), columns = vectorizer.get_feature_names())
        #df['source'] = headline_dict.keys()
        #df['headline'] = headline_dict.values()
        return df

class pickle_data():
    
    def pickle_data(self,data):
        headlines = data.headline_dict
        files = os.listdir('C:\\Users\\seoleary\\Desktop\\Programming\\Python')
        classified_pickle = [x for x in files if x.startswith('classify') and x.endswith('.pkl')]
        if len(classified_pickle)==0:
            file = open('C:\\Users\\seoleary\\Desktop\\Programming\\Python\\classify.pkl','wb')
        else:
            numbers = [int(x[8:len(x)-4]) for x in classified_pickle if x[8:len(x)-4].isdigit()]
            if len(numbers) == 0:
                number = 1
            else:
                number = max(numbers)+1
            file = open('C:\\Users\\seoleary\\Desktop\\Programming\\Python\\classify'+str(number)+'.pkl','wb')
        pickle.dump(data,file)
        file.close()        
#######################################################3
########################################################

data = collect_data()


