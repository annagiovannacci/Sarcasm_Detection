from pickle import TRUE
import ktrain
import ast
import os
from nltk.tree import ProbabilisticTree
from transformers import *
import tensorflow as tf
import explainability as E
import scraping
import re
import html
import torch
import time
from datetime import datetime



#Change "1" with "0,1" or "0" depending on which GPU you want to use
#os.environ["CUDA_VISIBLE_DEVICES"]="1"

MODEL_NAME = 'bert-base-multilingual-uncased'
BASE_DIR_WEIGHTS = ''

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(BASE_DIR_WEIGHTS+'weights//sarcasm',from_tf = True)
model_sl = AutoModel.from_pretrained(BASE_DIR_WEIGHTS+'weights//tweet-shot-e-first-format',from_tf = True)
model_2 = AutoModel.from_pretrained(BASE_DIR_WEIGHTS+'weights//long-text-predictor-first-format',from_tf=True)


predictor_long_text_second_format =  ktrain.load_predictor(BASE_DIR_WEIGHTS+'weights/long-text-predictor-second-format')
predictor_three_way_tweets = ktrain.load_predictor(BASE_DIR_WEIGHTS+'weights/tweet-shot-e-second-format')
predictor_tweets_binary = ktrain.load_predictor(BASE_DIR_WEIGHTS+'weights/Model-for-pred')

def preprocess_text(sentence):
    sentence = sentence.replace('\n','' ) #cleaning newline “\n” from the tweets
    sentence = re.sub(r'(@[A-Za-z_]+)|[^\w\s]|#|http\S+', '', sentence)
    sentence = html.unescape(sentence)
    return sentence


#check the explainability of the prediction of a sentence
def satire_prediction_explainability(sentence,scope):
  input_ids = tf.constant(tokenizer.encode(sentence,return_tensors='pt',add_special_tokens=False))
  if scope == 1:
    input_embeds, token_ids_tensor_one_hot = E.get_embeddings(input_ids,model)
  elif scope == 2:
    input_embeds, token_ids_tensor_one_hot = E.get_embeddings(input_ids,model_sl)

  output = model(inputs_embeds = input_embeds)
  predict = output.pooler_output
  token_importance_norm = E.gradient_x_inputs_attribution(predict,input_embeds).cpu().detach().numpy()


  token_ids = list(input_ids.numpy()[0])

  token_words = tokenizer.convert_ids_to_tokens(token_ids) 
  token_types = list(input_ids.numpy()[0])
  print(token_words)

  return token_importance_norm,token_words
def satire_prediction(sentence, scope,subscope):
  sentence = preprocess_text(sentence)
  if scope == 'long_text':
    predictor = predictor_long_text_second_format
  elif scope == 'satire':
    if subscope == 2:
      predictor = predictor_three_way_tweets
    elif subscope == 1:
      predictor = predictor_tweets_binary
      print(subscope)
  y = predictor.predict(sentence)
  probabilities = predictor.predict_proba(sentence)
  return y, probabilities
def long_text_prediction_explainability(text):
  input_ids = tf.constant(tokenizer.encode(text,return_tensors='pt',add_special_tokens=False))
  input_embeds, token_ids_tensor_one_hot = E.get_embeddings(input_ids,model_2)
  token_ids = list(input_ids.numpy()[0])
  if (input_embeds.size()[1]>512):
    print("--HERE")
    print(input_ids)
    input_ids = input_ids[0][0:512]
    print(input_ids)
    data = input_embeds.data[:,0:512,:]
    input_embeds = torch.FloatTensor(data)
    input_embeds = input_embeds.clone().requires_grad_(True)
  output = model_2(inputs_embeds = input_embeds)
  predict = output.pooler_output
  token_importance_norm = E.gradient_x_inputs_attribution(predict,input_embeds).cpu().detach().numpy()
  token_words = tokenizer.convert_ids_to_tokens(token_ids) 
  #token_types = list(input_ids.numpy()[0])
  print(token_words)
    
  return token_importance_norm,token_words


def debug():
  now = datetime.now()
  print("now =", now)




