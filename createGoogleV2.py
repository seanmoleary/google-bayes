# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:57:53 2019

@author: seoleary
"""

import pandas
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords

class createGoogle(object):
    
    def __init__(self):
        self.file = ""
        self.wordlist = {'espionage','lawsuit','law suit','sanctions','violations','corruption','negative','media', 'labor','safety','disruption','counterfeit','fraud','recall','ethics','compliance','dispute'}
        self.frame = None
        self.searchString = self.createSearchString()
        self.chromeDriverPath = r'C:\Users\seoleary\Desktop\Programming\Python\chromedriver.exe'
        self.browser = self.openBrowser()
        
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
    
    #does the selenium bit, opening a webbrowser and returning the browser object
    def openBrowser(self):
        browser =  webdriver.Chrome(executable_path = self.chromeDriverPath)
        browser.get(r'https://www.google.com')
        return browser
      
    #puts the search string into the webbrowser, updating the public webbrower object in this class
    def searchGoogle(self):
        search = self.browser.find_element_by_name('q')
        search.clear()
        search.send_keys(self.searchString)
        search.send_keys(Keys.RETURN)
    
    #updates the public search string in this class
    def setSearchString(self, toSearch):
        self.file = toSearch
        self.searchString = self.createSearchString()
     
    # Shows the number of results in the google search
    def showCount(self):
        source = self.browser.page_source
        soup = BeautifulSoup(source,'lxml')
        try:
            numText = soup.find('div',{'id':'resultStats'}).text
            remTime = numText[:numText.find('(')-1]
            numList = [int(i) for i in remTime if i.isdigit()]
            numStr = ''.join(map(str,numList))
            num = int(numStr)
        except:
            num = 0
        return num
    
    #gets the top ten words in the top ten google headlines
    ## NEEDS MORE WORK.. maybe read more than 10 headlines, maybe read the articles?
    def getWords(self):
        source = self.browser.page_source
        soup = BeautifulSoup(source,'lxml')
        headlines = soup.find_all('h3')
        headlines = [i.text for i in headlines]
        text = " ".join(headlines[:len(headlines)-1])
        textList = text.split(" ")
        punct = {',','-','.','...','|'}
        sWords = set(stopwords.words('english'))
        finalTextList = [x for x in textList if x not in punct if x not in sWords]
        fd = nltk.FreqDist(finalTextList)
        finalReturn = [x for x in fd]
        return finalReturn[:10]

#an excel file with a list of company names 
#toSearch = r'C:\Users\seoleary\Desktop\Programming\Python\createGoogle.xlsx'


supplierFrame = pandas.read_excel(r'C:\Users\seoleary\Desktop\mediaSups.xlsx')

l = []
a= []
obj = createGoogle()
counter = 0
for company in supplierFrame['Company']:
    
    # google will think you are a robot somewhere around 40 hits.. so this re-creates the search window
    if counter==30:
        obj=createGoogle()
        counter=0
    a = []
    a = [company]
    obj.setSearchString(company)
    obj.searchGoogle()
    count = obj.showCount()
    a.append(count)
    wordList = obj.getWords()
    for i in wordList:
        a.append(i)
    print("There were "+str(count)+" google results")
    print("THE MAJOR WORDS WERE : ",", ".join(wordList))
    print()
    l.append(a)
    counter=counter+1

df = pandas.DataFrame(l,columns = ['company','hits','term1','term2','term3',
                              'term4','term5','term6','term7','term8','term9','term10'])
    
df.to_excel(r'C:\Users\seoleary\Desktop\mediaSupsOut2.xlsx',index = False)
    
