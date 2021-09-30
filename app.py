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
        prediction_, probabilities = AFC.satire_prediction(sentence, 'satire')
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
    prediction,probabilities = AFC.satire_prediction(text,'long_text')
    if (prediction == 'FAKE'):
        probability = probabilities[0]
    if (prediction == 'REAL'):
        probability = probabilities[1]
    if (prediction == 'SATIRICAL'):
        probability = probabilities[2]
    probability = probability*100
    result = {'text_long':text, 'long_text_pred' : prediction, 'confidence': int(probability)}
    return jsonify(result)

@app.route('/multilingual_tweet')
def prediction_tweet():
    text = request.args.get('text',0,type=str)
    text = AFC.preprocess_text(text)
    prediction, probabilities = AFC.satire_prediction(text,'satire')
    if (prediction == 'SATIRE'):
        probability = probabilities[1]
    elif (prediction == 'NOT_SATIRE'):
        probability = probabilities[0]
    probability = probability * 100
    result = {'tweet':text,'tweet_pred':prediction,'confidence':int(probability)}
    return jsonify(result)
@app.route("/explain_prediction_single_tweet")
def explaination_prediction_single_tweet():
    tweet           = request.args.get('text', 0, type=str)
    print("prediction for text:", tweet)
    print("Explaining prediction for text: ", tweet)
    tweet = tweet.replace('\n','' ) #cleaning newline “\n” from the tweets
    sentence = re.sub(r'(@[A-Za-z_]+)|[^\w\s]|#|http\S+', '', tweet)
    sentence = html.unescape(sentence)
    token_importance_norm_, token_words_ = AFC.satire_prediction_explainability(sentence)
    max_exp = np.max(token_importance_norm_)
    min_exp = np.min(token_importance_norm_)
    s = (token_importance_norm_-min_exp) / (max_exp - min_exp+0.01)
    new_x = s.tolist() 
    print(sentence)
    prediction_, probabilities = AFC.satire_prediction(sentence, 'satire')
    result = {'text':tweet,'tokenization':token_words_,'explanation':new_x,'prediction': prediction_}
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