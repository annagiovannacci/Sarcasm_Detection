# from pickle import TRUE
from ktrain import load_predictor
# import ast
# import os
# from nltk.tree import ProbabilisticTree
from transformers import AutoTokenizer, AutoModel
from tensorflow import constant
import explainability as E
# import scraping
import re
import html
from torch import FloatTensor
# import time
from datetime import datetime
print("import AFC")

# Change "1" with "0,1" or "0" depending on which GPU you want to use
# os.environ["CUDA_VISIBLE_DEVICES"]="1"

MODEL_NAME = 'bert-base-multilingual-uncased'
BASE_DIR_WEIGHTS = ''
# BASE_DIR_WEIGHTS = '/mnt/g/.shortcut-targets-by-id/1SowylFaTfsAuRHKJRN7yE6AaIKIojvuz/ThesisMaterial/APP/'
# BASE_DIR_WEIGHTS = '//mnt//c//users//annag//desktop//sarcasmdetection//'

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(BASE_DIR_WEIGHTS+'weights//sarcasm',from_tf = True)
model_sl = AutoModel.from_pretrained(BASE_DIR_WEIGHTS+'weights//tweet-shot-e-first-format',from_tf = True)
model_2 = AutoModel.from_pretrained(BASE_DIR_WEIGHTS+'weights//long-text-predictor-first-format',from_tf=True)
print("first models imported")

predictor_long_text_second_format = load_predictor(BASE_DIR_WEIGHTS+'weights/long-text-predictor-second-format')
predictor_three_way_tweets = load_predictor(BASE_DIR_WEIGHTS+'weights/tweet-shot-e-second-format')
predictor_tweets_binary = load_predictor(BASE_DIR_WEIGHTS+'weights/Model-for-pred')
print("second models imported")

def preprocess_text(sentence):
    for a, b in zip(["à","è","é","ò","ì","ù","À","È","Ì","Ò","Ù","\n"],["a'","e'","e''","o'","i'","u'","A'","E'","I'","O'","U'"," "]):
      sentence = sentence.replace(a,b)
    sentence = re.sub(r'(@\S+)|[^\w\s]|#|http\S+', '', sentence)
    sentence = html.unescape(sentence)
    return sentence


# check the explainability of the prediction of a sentence
def satire_prediction_explainability(sentence,scope):
  input_ids = constant(tokenizer.encode(sentence,return_tensors='pt',add_special_tokens=True))
  if scope == 1:
    input_embeds, token_ids_tensor_one_hot = E.get_embeddings(input_ids,model)
  elif scope == 2:
    input_embeds, token_ids_tensor_one_hot = E.get_embeddings(input_ids,model_sl)

  output = model(inputs_embeds = input_embeds)
  predict = output.pooler_output
  token_importance_norm = E.gradient_x_inputs_attribution(predict,input_embeds).cpu().detach().numpy()

  
  token_ids = list(input_ids.numpy()[0])

  token_words = tokenizer.convert_ids_to_tokens(token_ids) 
  print(input_ids)
  print("---")
  print(token_words)

  return token_importance_norm,token_words

def satire_prediction(sentence, scope, subscope):
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
  input_ids = constant(tokenizer.encode(text,return_tensors='pt',add_special_tokens=True))
  input_embeds, token_ids_tensor_one_hot = E.get_embeddings(input_ids,model_2)
  token_ids = list(input_ids.numpy()[0])
  if (input_embeds.size()[1]>512):
    print("--HERE")
    print(input_ids)
    input_ids = input_ids[0][0:512]
    print(input_ids)
    data = input_embeds.data[:,0:512,:]
    input_embeds = FloatTensor(data)
    input_embeds = input_embeds.clone().requires_grad_(True)
    print(input_embeds.size())
  output = model_2(inputs_embeds = input_embeds)
  predict = output.pooler_output
  token_importance_norm = E.gradient_x_inputs_attribution(predict,input_embeds).cpu().detach().numpy()
  token_words = tokenizer.convert_ids_to_tokens(token_ids)[1:-1]
  #token_types = list(input_ids.numpy()[0])
  print(token_words, len(token_words))
    
  return token_importance_norm,token_words

def debug():
  now = datetime.now()
  print("now =", now)

