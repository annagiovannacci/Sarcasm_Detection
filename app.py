from flask import Flask, render_template, request, json, jsonify
import concurrent.futures
import csv
#from flask_ngrok import run_with_ngrok
import explainability as E
import AFC
import numpy as np
import pandas as pd
import scraping
import nltk
import re
import html
import spacy
import icecream as ic
import time
import datetime


nltk.download('punkt')

app = Flask(__name__, static_url_path='/static')
#run_with_ngrok(app)

"""

Returns the home page

"""
@app.route("/")
def main():
    return render_template('index.html',  analysis_requested = 0)

@app.route('/explain_prediction_sentence_by_sentence')
def explain_prediction_single():

    #Retrieve arguments sent by the client
    #predictor_name = request.args.get('predictor_name', 0, type=str)
    text           = request.args.get('text', 0, type=str)
    #divide the text in sentences
    sentences = scraping.split_into_sentences(text)
    token_importance_norm = []
    token_words = []
    explanation = []
    prediction = []

    for sentence in sentences:
        print("prediction for text:", sentence)
        print("Explaining prediction for text: ", sentence)
        sentence = AFC.preprocess_text(sentence)
        token_importance_norm_1, token_words_1 = AFC.satire_prediction_explainability(sentence)
        max_exp = np.max(token_importance_norm_1)
        min_exp = np.min(token_importance_norm_1)
        s = (token_importance_norm_1-min_exp) / (max_exp - min_exp+0.01)
        new_x = s.tolist() 
        token_importance_norm.append(token_importance_norm_1)
        token_words.append(token_words_1)
        explanation.append(new_x)
        print(sentence)
        prediction_, probabilities = AFC.satire_prediction(sentence, 'satire',None)
        prediction.append(prediction_)

    print(token_words)
    print(explanation)

    result = {'text':text,'tokenization':token_words,'explanation':explanation,'prediction': prediction}
    return jsonify(result)

@app.route('/prediction_long_text')
def prediction_long_text():

    text = request.args.get('text',0,type = str)

    print("Predicting for long text...")
    print(text)

    text = AFC.preprocess_text(text)
    prediction,probabilities = AFC.satire_prediction(text,'long_text',None)
    print(prediction)
    probability = np.max(probabilities)
    probability = probability*100
    result = {'text_long':text, 'long_text_pred' : prediction, 'confidence': int(probability)}

    return jsonify(result)

@app.route('/multilingual_tweet')
def prediction_tweet():

    text = request.args.get('text',0,type=str)
    scope = request.args.get('scope',0,type=int)
    text = AFC.preprocess_text(text)
    prediction, probabilities = AFC.satire_prediction(text,'satire',scope)

    print(scope)

    probability = np.max(probabilities)

    probability = probability * 100
    result = {'tweet':text,'tweet_pred':prediction,'confidence':int(probability)}

    return jsonify(result)

@app.route("/explain_prediction_single_tweet")
def explaination_prediction_single_tweet():
    
    tweet = request.args.get('text', 0, type=str)
    scope = request.args.get('scope',0,type=int)
    
    print("prediction for text:", tweet)
    print("Explaining prediction for text: ", tweet)
    
    tweet = tweet.replace('\n','' ) #cleaning newline “\n” from the tweets
    sentence = re.sub(r'(@[A-Za-z_]+)|[^\w\s]|#|http\S+', '', tweet)
    sentence = html.unescape(sentence)
    token_importance_norm_, token_words_ =  AFC.satire_prediction_explainability(sentence,scope)
    print(AFC.debug())
    max_exp = np.max(token_importance_norm_)
    min_exp = np.min(token_importance_norm_)
    s = (token_importance_norm_-min_exp) / (max_exp - min_exp+0.01)
    new_x = s.tolist() 
   
    print(sentence)
    
    prediction_, probabilities = AFC.satire_prediction(sentence, 'satire',scope)
    result = {'text':tweet,'tokenization':token_words_,'explanation':new_x,'prediction': prediction_}
    print(AFC.debug())
    return jsonify(result)

@app.route('/explain_prediction')
def explain_prediction():
    
    long_text = request.args.get('text', 0, type=str)
    
    print("prediction for text:", long_text)
    print("Explaining prediction for text: ", long_text)
    
    text = AFC.preprocess_text(long_text)
    token_importance_norm_, token_words_ = AFC.long_text_prediction_explainability(text)

    token_importance_norm_ = log_log(token_importance_norm_,7)
    
    max_exp = np.max(token_importance_norm_)
    min_exp = np.min(token_importance_norm_)
    
    #print(max_exp)
    
    s = (token_importance_norm_-min_exp) / (max_exp - min_exp + 0.01)
    new_x = s.tolist() 
    
    print(text)
    
    prediction_, probabilities = AFC.satire_prediction(text, 'long_text',None)
    
    result = {'text':long_text,'tokenization':token_words_,'explanation':new_x,'prediction': prediction_}
    
    return jsonify(result)

@app.route("/get_example")
def get_ex():
    label = request.args.get('label',0,type=str)
    d = pd.read_csv('examples/satirical_dat.csv')
    d.dropna(subset=['text'],inplace=True)
    d.reset_index(inplace=True)
    text = str(d[d['label']==label].sample(n=1)['text'].iloc[0])
    
    if (len(text)>=4094):
        text = text[:4094]
    
    return jsonify({'example': text})

@app.route("/get_worst_predictions")
def get_wp():

    d = pd.read_csv('examples/worst_predictions_23_.csv')
    d.dropna(subset=['Text'],inplace=True)
    d.reset_index(inplace=True)
    sample = d.sample(n=1)    
    text = str(sample.Text.iloc[0])
    label = str(sample.Label.iloc[0])
    if label == "0":
        label = "REAL"
    elif label == "1":
        label = "SATIRICAL"
    else:
        label = "FAKE"
    return jsonify({'example': text,'label':label})

@app.route("/get_ironic_examples")
def get_ex_2():
    
    label = request.args.get('label',0,type=str)
    d = pd.read_csv('examples/twittiro.csv', delimiter='\t')
    d.dropna(subset=['text'],inplace=True)
    d.reset_index(inplace=True)
    text = str(d.sample(n=1)['text'].iloc[0])
    
    if (len(text)>=4094):
        text = text[:4094]
    
    nlp = spacy.load("it_core_news_sm")
    doc = nlp(AFC.preprocess_text(text))
    s = ''
    
    for w in doc:
        s += w.text + ":\t" + w.pos_ + "\n"
    
    print(s)

    return jsonify({'example': text,'doc':s})

"""

Returns a text that can be used as example by the user
The text can be one of the examples prepared by us or a transcript from a random Trump speech (thanks to rev.com)

Returns "About us" page

"""
@app.route('/about.html')
def show_about():
    return render_template('about.html')

"""

Return explanations for the various models

"""
@app.route('/bias.html')
def show_bias():
    return render_template('bias.html')

@app.route('/ideology.html')
def show_ideology():
    return render_template('ideology.html')

def time_format():
    return f'{datetime.now()}|> '

def log_plus(x):
    return np.log(x + 1)

def log_log(x,t=3):
    y = x
    for i in range(t):
        y = log_plus(y)
    return y

'''
Runs the application server side'''

if __name__ == "__main__":
    app.run(host='0.0.0.0')

#app.run()