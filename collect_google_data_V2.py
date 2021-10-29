# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 15:32:54 2019

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
    Collects training data from google searches 
    
    Lets the user identify which articles fall in the categories
        1 - Negative News
        0 - Not-Negative
        
        -> FUTURE FUNCTIONALITY SHOULD INCLUDE MULTI_CLASS CLASSIFICATION
            TO IDENTIFY CERTAIN TYPES OF NEGATIVE NEWS
            (I.E. CYBER VULNERABILITY, CORRUPTION, FOREIGN INFLUENCE)
        
    """
    
    def __init__(self):
        self.numResults, self.language = 10 , 'en'
        self.companies = self.get_companies()
        self.keywords = self.set_keywords()
        self.headline_dict = self.get_words_remove_company(self.companies,self.keywords)
        self.Y = self.classify(self.headline_dict)
        
        
    def get_companies(self, test_train = 'train'):
        '''
        Asks the user which companies they want to collect data with
        '''
        
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
        '''
        Asks the user which google search keywords they want to train with
        '''
        
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
        '''
        Creates the search string for google searching
        
        '''
        search_string = '"'+company+'"+AND+"'+keyword+'"'
        return search_string        
    
    def get_google(self, company, term):
        '''
        Uses the requests package to retrieve google search results
        '''
        search_term = self.make_search_string(company, term)
        googleUrl = 'https://www.google.com/search?q={}&num={}&hl={}&tbm=nws'.format(search_term, self.numResults, self.language)
        response = requests.get(googleUrl)
        response.raise_for_status()
        soup = BeautifulSoup(response.text,'lxml')
        headlines = soup.find_all('div', attrs={'class':'g'})
        # returns a list of google tagged html data
        return headlines
      
    def get_words_remove_company(self, companies, keywords): 
        '''
        processes the google tagged html data to 
        1. identify the URL
        2. extract the headline and blurb
        3. make a dictionary with key:value == URL:text
        4. substitute the term "company_name" for the actual name of the company
            - this makes the classifer agnostic of the particular company
            - this puts less bias on particular companies
        '''
        headline_dict = {}
        for company in companies:
            for keyword in keywords:
                headlines = self.get_google(company,keyword)
                for k in headlines:
                    key = k.find('a',href=True)['href'][7:]
                    if key not in headline_dict.keys() and k.text not in headline_dict.values():
                        text = k.text
                        text = text.replace('\xa0', ' ')
                        
                        # Make sure that the specific company name does not affect
                        # the classifier, but instead that the presence of a company name will 
                        # still hold more weight when classifying an unknown set of data
                        text = text.replace(company, 'COMPANY_NAME')
                        headline_dict[key] = text
        #returns a dictionary where key:value == URL:text
        return headline_dict
    
    def classify(self, headline_dict):
        '''
        Asks the user to classify each news object as either 
            Y - Negative News
            N - Non-Negative News
        '''
        Y = []
        print("Is this negative news? Type 'Y' for negative news and 'N' for non-negative news'\n'")
        for i in headline_dict.values():
            print(i)
            classified = str(input())
            while classified.lower()!='y' and classified.lower()!='n':
                classified = str(input("PLEASE TYPE 'Y' OR 'N'"))
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
    
    def model(self, model_type = 'mnb'):
        '''
        lets user define which type of model they want to train with
        
        '''
        if model_type == 'logit':
            pass
        elif model_type == 'svm':
            pass
        else:
            pass
        pass
    
    def pipeline(self, data):
        '''
        instead of piecemeal processing/prediction, use a pipeline
        '''
        pass
    

class pickle_data():
    
    '''
    stores data on machine.. needs to be completed
    '''
    def pickle_data(self,data):
        #headlines = data.headline_dict
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

    def unpickle_data(self):  
        self
#######################################################3
########################################################

data = collect_data()
'''
TO DO 
1. Figure out a way to put a space between the headline and the blurb
2. Better data structure to house headline, blurb, url, class
    - maybe just a DF
3. Create pipeline
    - compare countvectorizer to tfidfvectorizer
    - compare svd, mnb, logistic
4. Identify if a multi class solution should be considered
    - example, classes for tech news, corruption, fines, etc.. 
5. Is the word2vec model usefule? with neural nets?
6. Jupyter notebooks
7. Rework the get_google() bit to retrieve from the API
'''