# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 15:59:47 2018

@author: seoleary

Opens a web browser with a google search of negative news regarding a company
"""
import pandas
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class createGoogle(object):
    
    def __init__(self, file):
        self.file = file
        self.wordlist = {'cyber','cyber-security','cyber security','bankruptcy','default','law suit','lawsuit'}
        self.frame = None
        if '.xlsx' in file:
            self.frame = pandas.read_excel(self.file)
        self.searchString = self.createSearchString()
        self.chromeDriverPath = r'C:\Users\seoleary\Desktop\Programming\Python\chromedriver.exe'
        
    def createSearchString(self):
        x,y = "(","("
        if type(self.frame) == pandas.core.frame.DataFrame:
            for i,name in enumerate(self.frame['company']):
                if i!=len(self.frame['company'])-1:
                    x += "\""+name+"\"" + " OR "
                else: 
                    x += "\""+name+"\""
        else:
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
    
    def openBrowser(self):
        browser =  webdriver.Chrome(executable_path = self.chromeDriverPath)
        browser.get(r'https://www.google.com')
        search = browser.find_element_by_name('q')
        search.send_keys(self.searchString)
        search.send_keys(Keys.RETURN)
        
    def printString(self):
        print(self.searchString)

#an excel file with a list of company names 
#toSearch = r'C:\Users\seoleary\Desktop\Programming\Python\createGoogle.xlsx'


toSearch = 'Serco'
obj = createGoogle(toSearch)
obj.openBrowser()
