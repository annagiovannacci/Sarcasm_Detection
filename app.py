from flask import Flask, render_template, request, json, jsonify
import concurrent.futures
import csv
#from flask_ngrok import run_with_ngrok
import explainability as E
import AFC
import numpy as np
import scraping
import nltk
import re
import html
nltk.download('punkt')



app = Flask(__name__, static_url_path='/static')
#run_with_ngrok(app)

"""

Returns the home page

"""
@app.route("/")
def main():
    return render_template('index.html',  analysis_requested = 0)

@app.route('/explain_prediction')
def explain_prediction():

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
        sentence = sentence.replace('\n','' ) #cleaning newline “\n” from the tweets
        sentence = re.sub(r'(@[A-Za-z_]+)|[^\w\s]|#|http\S+', '', sentence)
        sentence = html.unescape(sentence)
        token_importance_norm_1, token_words_1 = AFC.satire_prediction_explainability(sentence)
        max_exp = np.max(token_importance_norm_1)
        min_exp = np.min(token_importance_norm_1)
        s = (token_importance_norm_1-min_exp) / (max_exp - min_exp)
        new_x = s.tolist() 
        token_importance_norm.append(token_importance_norm_1)
        token_words.append(token_words_1)
        explanation.append(new_x)
        prediction.append(AFC.satire_prediction(sentence,'satire'))
    print(token_words)
    print(explanation)
    result = {'text':text,'tokenization':token_words,'explanation':explanation,'prediction': prediction}
    return jsonify(result)

@app.route('/prediction_long_text')
def prediction_long_text():
    text = request.args.get('text',0,type = str)
    print("Predicting for long text...")
    prediction = AFC.satire_prediction(text,'long_text')
    result = {'text_long':text, 'long_text_pred' : prediction}
    return jsonify(result)

@app.route('/multilingual_tweet')
def prediction_tweet():
    text = request.args.get('text',0,type=str)
    print("predicting our tweet..")
    prediction = AFC.satire_prediction(text,'satire')
    result = {'tweet':text,'tweet_pred':prediction}
    return jsonify(result)




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


'''
Runs the application server side'''

if __name__ == "__main__":
    app.run(host='0.0.0.0')

#app.run()