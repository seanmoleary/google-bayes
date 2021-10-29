# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 19:45:53 2019

@author: seoleary

This is a latest version of the google search for a company's negative news results

The program:
    1. Uses a list of words and a company name to create a google search string
    2. Using requests, gets the html for the top 60 google news results
    3. Removes all of the stopwords and punctuation and lower cases everything
    4. Returns the top 50 most common words
    
"""

import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

class createGoogle(object):
    
    def __init__(self, file):
        self.file = file
        self.numResults = 60
        self.language = 'en'
        self.wordlist = {}
        self.searchString = self.createSearchString()
        
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
    
    #returns a list of tuples of the top 50 words in the 60 google news headlines
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
        sWords = set(stopwords.words('english'))
        finalTextList = [x for x in words if x.isalpha() if x not in sWords]
        fd = nltk.FreqDist(finalTextList)
        top = fd.most_common(50)
        finalReturn = [x for x in top]
        return text, finalReturn

def main():
    stopwords = set(STOPWORDS)
    obj = createGoogle(input("What Company?: "))
    words, dic = obj.getWords()
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(words)
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
      
    plt.show()
    
if __name__ == '__main__':
    main()