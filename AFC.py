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


#Change "1" with "0,1" or "0" depending on which GPU you want to use
#os.environ["CUDA_VISIBLE_DEVICES"]="1"

MODEL_NAME = 'bert-base-multilingual-uncased'
BASE_DIR_WEIGHTS = '//mnt//c//users//annag//Desktop//SarcasmDetection//'

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(BASE_DIR_WEIGHTS+'weights//sarcasm',from_tf = True)
model_2 = AutoModel.from_pretrained(BASE_DIR_WEIGHTS+'weights/long-text-predictor-first-format',from_tf=True)

def preprocess_text(sentence):
    sentence = sentence.replace('\n','' ) #cleaning newline “\n” from the tweets
    sentence = re.sub(r'(@[A-Za-z_]+)|[^\w\s]|#|http\S+', '', sentence)
    sentence = html.unescape(sentence)
    return sentence


#check the explainability of the prediction of a sentence
def satire_prediction_explainability(sentence):
  input_ids = tf.constant(tokenizer.encode(sentence,return_tensors='pt',add_special_tokens=False))
  input_embeds, token_ids_tensor_one_hot = E.get_embeddings(input_ids,model)
  output = model(inputs_embeds = input_embeds)
  predict = output.pooler_output
  token_importance_norm = E.gradient_x_inputs_attribution(predict,input_embeds).cpu().detach().numpy()


  token_ids = list(input_ids.numpy()[0])

  token_words = tokenizer.convert_ids_to_tokens(token_ids) 
  token_types = list(input_ids.numpy()[0])
  print(token_words)

  return token_importance_norm,token_words
def satire_prediction(sentence, scope):
  sentence = preprocess_text(sentence)
  if scope == 'long_text':
    predictor = ktrain.load_predictor(BASE_DIR_WEIGHTS+'weights/long-text-predictor-second-format')
  elif scope == 'satire':
    predictor = ktrain.load_predictor(BASE_DIR_WEIGHTS+'weights/Model-for-pred')
  y = predictor.predict(sentence)
  probabilities = predictor.predict_proba(sentence)
  return y, probabilities
def long_text_prediction_explainability(text):
  input_ids = tf.constant(tokenizer.encode(text,return_tensors='pt',add_special_tokens=False))
  input_embeds, token_ids_tensor_one_hot = E.get_embeddings(input_ids,model_2)
  output = model_2(inputs_embeds = input_embeds)
  predict = output.pooler_output
  token_importance_norm = E.gradient_x_inputs_attribution(predict,input_embeds).cpu().detach().numpy()


  token_ids = list(input_ids.numpy()[0])

  token_words = tokenizer.convert_ids_to_tokens(token_ids) 
  token_types = list(input_ids.numpy()[0])
  print(token_words)  
  return token_importance_norm,token_words



