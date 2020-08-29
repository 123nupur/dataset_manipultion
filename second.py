# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


import requests 
URL = "http://www.values.com/inspirational-quotes"
r = requests.get(URL) 
print(r.content) 

from bs4 import BeautifulSoup 
soup = BeautifulSoup(r.content, 'html5lib') 
print(soup.prettify()) 

import csv
quotes=[]  # a list to store quotes 
  
table = soup.find('div', attrs = {'class':"row",'id':"all_quotes"}) 
for rows in table.findAll('div', attrs = {'class':"col-6 col-lg-3 text-center margin-30px-bottom sm-margin-30px-top"}): 
    quote = {} 
    quote['theme'] = rows.h5.text 
    quote['url'] = rows.a['href'] 
    quote['img'] = rows.img['src']  
    quote['lines'] = rows.img['alt']
    quotes.append(quote) 
filename = 'inspirational_quotes.csv'
with open(filename, 'a') as f: 
    w = csv.DictWriter(f,['theme','url','img','lines','author']) 
    w.writeheader() 
    for quote in quotes: 
        w.writerow(quote)
df=pd.read_csv("inspirational_quotes.csv")
display(df)


