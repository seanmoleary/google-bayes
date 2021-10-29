# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 12:47:52 2019

@author: seoleary
The program:
    1. Input a company name
    2. searches google for that company name 
    3. Creates a frequency distribution of each word
    4. Creates an input for the bayes classifier 
    5. Compares to the bayes classifier
    
Dosesn't yet allow for using new headlines against the classifier

"""

import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split


class create_google(object):
    
    def __init__(self, file):
        self.file = file
        self.numResults = 60
        self.language = 'en'
        self.wordlist = {'corruption','vulnerability','lawsuit','fines'}
        self.searchString = self.createSearchString()
        self.headlines,self.words_dict = self.getWords()
        self.matrix = self.make_matrix()
        
        
    #creates a giant search string to put into google    
    def createSearchString(self):
        x,y = "(","("
        x+='"'+self.file+'"'
                        
        for i,name in enumerate(self.wordlist):
            if i!=len(self.wordlist)-1:
                y += "\""+name+"\"" + " OR "
            else: 
                y += "\""+name+"\""        
        x+=")"
        y+=")"        
        finalString = x + " AND " +y
        
        return finalString
    
    #returns the headlines and frequency distribution of the words in the 60 google news headlines
    def getWords(self):
        googleUrl = 'https://www.google.com/search?q={}&num={}&hl={}&tbm=nws'.format(self.searchString, self.numResults, self.language)
        response = requests.get(googleUrl)
        response.raise_for_status()
        soup = BeautifulSoup(response.text,'lxml')
        headlines = soup.find_all('div', attrs={'class':'g'})
        headlines = [i.text for i in headlines]
        text = " ".join(headlines)
        words = nltk.word_tokenize(text)
        words = [i.lower() for i in words]
        sWords = set(stopwords.words('english')+self.file.lower().split())
        finalTextList = [x for x in words if x.isalpha() if x not in sWords]
        fd = nltk.FreqDist(finalTextList)
        return headlines, dict(fd)

    #creates a row for each headline that indicates the frequency of of its words
    #in regards to all possible words used
    ## also has the user attach a classification of 1 of 0 
    def make_matrix(self):
        words = self.words_dict.keys()
        rows = []
        for headline in self.headlines:
            row = []
            print(headline)
            is_negative = input("Good or bad: 1 or 0? ")
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


###########################################################
########################################################### 
## WORKING CODE STARTS HERE
        
#creates the bag of words for the company you want to train the model for
obj = create_google(input("What Company?: "))
columns = ["Negative"]+list(obj.words_dict.keys())
df = pd.DataFrame(obj.matrix, columns = columns)

#sets the training and test data
x_train ,x_test = train_test_split(df,test_size=0.5)
y_train = x_train["Negative"]
x_train = x_train.iloc[:,1:]
y_test = x_test["Negative"]
x_test = x_test.iloc[:,1:]

#initializes and fits the Multinomial Bayes model
mb = MultinomialNB()
fit = mb.fit(x_train,y_train)

#determines mislabled points for the training data against the modesl
y_train_predict = fit.predict(x_train)
points = y_train.shape[0]
mislabled = (y_train != y_train_predict).sum()
print("Number of training data points mislabeled out of a total %d points : %d ... percent wrong = %d"% (points,mislabled,round(mislabled/points*100,2)))

#determines the mislabeled points for the test data
y_test_predict = fit.predict(x_test)
points = y_test.shape[0]
mislabled = (y_test != y_test_predict).sum()
print("Number of training data points mislabeled out of a total %d points : %d ... percent wrong = %d"% (points,mislabled,round(mislabled/points*100,2)))

    
