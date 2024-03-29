# -*- coding: utf-8 -*-
"""NewsClassification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZpM4iP9AJBdo-LhzIUeuXm9tVniK_6IR
"""

from google.colab import drive
drive.mount('/content/drive')

!ls '/content/drive/My Drive/Colab Notebooks/News_Category_Dataset_v2.json'

!pip install -q xlsxwriter

import re
import json
import nltk
import xlsxwriter
import pandas as pd
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def ReadJson(filename):
    with open(filename) as f:
        data = [json.loads(line) for line in f] 
    return data
  
def CleanText(text):
  return re.sub('\W+',' ', text)


def Tokenize(text):
  return word_tokenize(text)


def Stemmer(word_list):
  ps = PorterStemmer()
  word_list = list(map(lambda word: ps.stem(word), word_list))
  return word_list 

def RemoveStopWords(word_list):
  word_list = list(filter(lambda word: word.lower() not in stopwords.words('english'), word_list))
  return word_list


def Count(word_list):
  counts = dict()
  for word in word_list:
    if word in counts:
      counts[word] += 1
    else:
      counts[word] = 1
  return counts
  

def AggregateText():
  data = ReadJson(filename)
  AggregatedText = ''
  
  for dictionary in data:
      AggregatedText += ' '+ dictionary['short_description'] +' '+ dictionary['headline']
  AggregatedText = CleanText(AggregatedText)
  Tokens = Tokenize(AggregatedText)
  
  # If we want to implement Stemming of words and removing stop words such as 'am', 'is', 'are', 'was', 'were'. 
  # StemmedText = Stemmer(Tokens)
  # OutText = RemoveStopWords(StemmedText)
  # return OutText
  
  return Tokens

def Onegram():
  Onegram.tokens = AggregateText()
  return Count(Onegram.tokens)
  
  
def Bigram(): 
  Bigrams = [Onegram.tokens[i] +' ' +Onegram.tokens[i+1] for i in range(0,len(Onegram.tokens)-1)]
  return Count(Bigrams)

  
def Output():
  Onegrams = Onegram()
  df_Onegrams = pd.DataFrame()
  df_Onegrams['Word']  = Onegrams.keys()
  df_Onegrams['Count'] = Onegrams.values()
  Bigrams = Bigram()
  df_Bigrams = pd.DataFrame()
  df_Bigrams['Word']  = Bigrams.keys()
  df_Bigrams['Count'] = Bigrams.values()
  return df_Onegrams , df_Bigrams

def PrintToExcel():
  df1,df2 = Output()
  writer = pd.ExcelWriter('Ngrams.xlsx', engine='xlsxwriter')
  df1.to_excel(writer, sheet_name='Sheet1',index=False)
  df2.to_excel(writer, sheet_name='Sheet2',index=False)
  writer.save()


if __name__ == '__main__':
  filename = ('/content/drive/My Drive/Colab Notebooks/News_Category_Dataset_v2.json')
  PrintToExcel()
