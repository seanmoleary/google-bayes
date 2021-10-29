# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 19:46:45 2019

@author: seoleary

An intermediary version of the create google program

Using requests vs Selenium to get content
"""
import requests
from bs4 import BeautifulSoup

def createGoogle(searchTerm, numResults=100, language = 'en'):
    assert isinstance(searchTerm, str)
    assert isinstance(numResults, int)
    searchTerm = searchTerm.replace(' ','+')
    googleUrl = 'https://www.google.com/search?q={}&num={}&hl={}'.format(searchTerm, numResults, language)
    response = requests.get(googleUrl)
    response.raise_for_status()
    return searchTerm, response.text

keyword, html = createGoogle('"Mack Trucks" "violation"')
soup = BeautifulSoup(html,'lxml')
table = soup.find_all('div', attrs={'class':'g'})    
