# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 12:47:52 2019

@author: seoleary

This is an initial Multinomil Bayes classifier for google headline article

The program retrieves 
"""

import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pickle


#new version of the program
#need to ...
# 1. create the classifier
# 2. input new companies' articles and compare against this model

class collect_data(object):
    """
    Collects either training data, or validation data. 
    
    If training data is collected, lets the user identify which articles fall in the categories
        1 - Negative News
        0 - Not-Negative
        
    If validation data is collected, doesn't require input
    """
    
    def __init__(self):
        self.numResults, self.language = 20 , 'en'
        self.companies = self.get_companies()
        self.keywords = self.set_keywords()
        self.search_string = self.make_search_string(self.companies,self.keywords)
        self.headlines, self.freq_dict = self.get_words(self.search_string, self.companies)
        self.training_matrix = self.make_training_matrix(self.freq_dict.keys(),self.headlines)
        self.classifier = self.mnb(self.training_matrix,self.freq_dict.keys())
        
    def get_companies(self, test_train = 'train'):
        x = []
        question = 'What company do you want to '+test_train+' with? '
        x.append(input(question))
        more = input('Another Company? (Y or N) ')
        while more == 'Y':
            company = input('Company name? ')
            x.append(company)  
            more = input('Another Company? (Y or N) ')            
            while more != ('Y' and 'N'):
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
            while other != ('Y' and 'N'):
                other = input('Please type Y or N ')
        return keywords
    
    def make_search_string(self,companies,keywords):
        #companies and keywords are lists
        companies = [i.replace(' ','+') for i in companies]
        companies = ['"'+i+'"' for i in companies]
        search_string = '%28'+'+OR+'.join(companies)+'%29+AND+'
        keywords = [i.replace(' ','+') for i in keywords]
        keywords = ['"'+i+'"' for i in keywords]
        search_string += '%28'+'+OR+'.join(keywords)+'%29'
        return search_string
        
    def get_words(self,search_string, companies):
        googleUrl = 'https://www.google.com/search?q={}&num={}&hl={}&tbm=nws'.format(search_string, self.numResults, self.language)
        response = requests.get(googleUrl)
        response.raise_for_status()
        soup = BeautifulSoup(response.text,'lxml')
        headlines = soup.find_all('div', attrs={'class':'g'})
        #THE FOLLOWING FINDS THE URLS FOR THE HEADLINES
        #url =[x.find('a',href=True)['href'][7:] for x in headlines]
        headlines = [i.text for i in headlines]
        text = " ".join(headlines)
        words = nltk.word_tokenize(text)
        words = [i.lower() for i in words]
        sWords = set(stopwords.words('english')+[i.lower() for i in companies])
        finalTextList = [x for x in words if x.isalpha() if x not in sWords]
        fd = nltk.FreqDist(finalTextList)
        return headlines, dict(fd)
    
    def make_training_matrix(self,keys,headlines):
        words = keys
        rows = []
        for headline in headlines:
            row = []
            print(headline)
            is_negative = input("Negative: 1 or Positive: 0? ")
            print()
            row.append(is_negative)
            tokenized_words = nltk.word_tokenize(headline)
            fd = nltk.FreqDist(tokenized_words)
            for w in words:
                if w in tokenized_words:
                    row.append(fd[w])
                else:
                    row.append(0)
            rows.append(row)
        return rows
    
    def mnb(self, training_matrix, keys):
        columns = ["Negative"]+list(keys)
        df = pd.DataFrame(training_matrix, columns = columns)
        
        x_train ,x_test = train_test_split(df,test_size=0.5)
        y_train = x_train["Negative"]
        x_train = x_train.iloc[:,1:]
        y_test = x_test["Negative"]
        x_test = x_test.iloc[:,1:]
        mb = MultinomialNB()
        fit = mb.fit(x_train,y_train)
        
        y_test_predict = fit.predict(x_test)
        points = y_test.shape[0]
        mislabled = (y_test != y_test_predict).sum()
        print("Number of test data points mislabeled out of a total %d points : %d ... percent wrong = %d"% (points,mislabled,round(mislabled/points*100,2)))
        print()
        
        return mb
        
    def validation_companies(self):
        companies = self.get_companies('test')
        search_string = self.make_search_string(companies,self.keywords)
        headlines,fd = self.get_words(search_string, companies)
        return headlines, fd
    
    def make_validation_matrix(self, headlines):
        words = self.freq_dict.keys()
        rows = []
        for headline in headlines:
            row = []
            tokenized_words = nltk.word_tokenize(headline)
            fd = nltk.FreqDist(tokenized_words)
            for w in words:
                if w in tokenized_words:
                    row.append(fd[w])
                else:
                    row.append(0)
            rows.append(row)
        return rows
    
######################
# Working Code

obj = collect_data()
headlines,fd = obj.validation_companies()    
rows = obj.make_validation_matrix(headlines)
a = obj.classifier.predict(rows)

for i,j in enumerate(a):
    if j==str(1):
        print(headlines[i])
        print()
       
p = pickle.Pickler()