from re import VERBOSE
import snscrape.modules.twitter as sntwitter
import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup

import nltk
nltk.download('punkt')
from nltk import tokenize

DEBUG = False


def obtain_tweet_by_user(username,NUM_TWEETS,label):
    
    # Creating list to append tweet data to
    tweets_list1 = []
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:'+username).get_items()):
        if i>NUM_TWEETS:
            break
        tweets_list1.append([tweet.content,label])
    # Creating a dataframe from the tweets list above
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Text','Label'])
    tweets_df1.to_csv(username+".csv")
    return tweets_df1

def scrapText(url): 
  data = requests.get(url)
  results = BeautifulSoup(data.content, 'html.parser')
  links = results.find_all("a",{"class":"sc-1out364-0 hMndXN js_link"})
  if (url =='https://www.theonion.com/breaking-news/news-in-brief'):
    links = links[12:]
  else:
    links = links[12:39]
  visits = []
  for l in range(len(links)):
    words = links[l]['data-ga'].split(",")
    link = words[2].replace('"','')
    visits.append(link)
  visits = set(visits)
  articles = []
  for url in visits:
    data = requests.get(url)
    text = BeautifulSoup(data.content, 'html.parser')
    article = text.find("p",{"class":"sc-77igqf-0 bOfvBY"})
    articles.append(['NOTITLE',article.text, "SATIRICAL"])
  return articles


def split_into_sentences(text):
  list_ = tokenize.sent_tokenize(text)
  return list_
 

def _similarity(text,predictor, satirical_predictor):
  label = predictor.predict(text)
  print("Label by model:")
  print(label)
  words = split_into_sentences(text)
  for word in words:
    labelled_ = satirical_predictor.predict(word)
    if labelled_ == 'SATIRE':
      count_satirical = count_satirical + 1
    else:
      count_not_satirical = count_satirical + 1
  print(count_satirical)
  print("non satirical sentences")
  print(count_not_satirical)

if DEBUG:
    NUM_TWEETS = 100
    username = "spinozait"
    tweets_sarcasm = obtain_tweet_by_user(username,NUM_TWEETS = NUM_TWEETS,label='SARCASTIC')
    print(tweets_sarcasm.head(1))