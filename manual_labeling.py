from AFC import satire_prediction_explainability, satire_prediction, preprocess_text, long_text_prediction_explainability
import pandas as pd
import numpy as np
from re import sub
from html import unescape
from spacy import load
from tqdm import tqdm
print("import man_l")

def explaination_prediction_single_tweet(sentence,tweet):
    # print("Explaining...")
    # tweet = request.args.get('text', 0, type=str)
    scope = 1 #request.args.get('scope',0,type=int)
    
    # print("Prediction for text:", tweet)
    # print("Explaining prediction for text: ", tweet)
    
    # sentence = preprocess_text(tweet)
    token_importance_norm_, token_words_ = satire_prediction_explainability(sentence,scope)
    max_exp = np.max(token_importance_norm_)
    min_exp = np.min(token_importance_norm_)
    s = (token_importance_norm_ - min_exp) / (max_exp - min_exp + 0.01)
    new_x = s.tolist() 
    
    
    # prediction_, probabilities = AFC.satire_prediction(sentence, 'satire',scope)
    result = {'text':tweet,'tokenization':token_words_,'explanation':new_x} #,'prediction': prediction_}
    
    return result

def prediction_tweet(text):

    # print("predicting...")

    # text = request.args.get('text',0,type=str)
    scope = 1 #request.args.get('scope',0,type=int)
    # text = preprocess_text(text)
    prediction, probabilities = satire_prediction(text,'satire',scope)

    if (prediction == 'SATIRE'):
        probability = probabilities[1]
    elif (prediction == 'NOT_SATIRE'):
        probability = probabilities[0]
    elif (prediction =='FAKE'):
        probability = probabilities[2]

    probability = probability * 100
    result = {'tweet':text,'tweet_pred':prediction,'confidence':int(probability)}

    return result

def manual_labeling(tweets_csv, dest_file=""):
    df = pd.read_csv(tweets_csv)
    ind = int(open("ind.txt","r").read())
    with open(dest_file,"a") as f:
        for tw in df.Text.iloc[ind:]:
            print("\nText:",tw)
            pred = prediction_tweet(tw)
            print("\nPred:",pred)
            expl = explaination_prediction_single_tweet(tw)
            print()
            for i in range(len(expl["explanation"][0])):
                print(expl["tokenization"][i],": \t",expl["explanation"][0][i])

            fr1 = input("Inserisci la prima fig ret: ")
            fr2 = input("Inserisci la seconda fig ret: ")
            map_s = input("1 se entrambe, 0.5 se una sola, 0 se nessuna: ")

            fr1 = "none" if fr1 == '' else fr1
            fr2 = "none" if fr2 == '' else fr2

            f.write('"'+tw+'",'+fr1+","+fr2+","+map_s)
            ind += 1
            end = input("Press any to go to next, or 'END' to close: ")
            if end == "END":
                open("ind.txt","w").write(str(ind))

def most_relevant_pos(df,dest_file="./pos.csv"):
    nlp = load("it_core_news_sm")
    pos_dict = {"pos":[],"saliency":[],"prediction":[]}
    input("Start? ")
    for text in tqdm(df.Text.iloc[:]):
        assert len(pos_dict["pos"]) == len(pos_dict["saliency"]) and len(pos_dict["pos"]) == len(pos_dict["prediction"])
        sentence = preprocess_text(text)
        if len(sentence) > 0 and not sentence.isspace():
            doc = nlp(sentence)
            pred = prediction_tweet(sentence)
            expl = explaination_prediction_single_tweet(sentence,text)
            # print("Tokens:")
            sent = ""
            expl_list = []
            count = 1
            for i in range(len(expl["tokenization"])):
                # print(expl["tokenization"][i])
                ex = float(expl["explanation"][0][i])
                if "#" not in expl["tokenization"][i]:
                    tok = " " + expl["tokenization"][i]
                    count = 1
                    expl_list.append(ex/count)
                    # print(tok, "\t", ex)
                else:
                    tok = expl["tokenization"][i].replace("##","")
                    expl_list[-1] = (expl_list[-1] * count + ex) / (count + 1)
                    count += 1
                    # print(tok, "\t", ex)
                sent += tok
            sent = sent[1:]
            # print(len(expl_list),len(sent.split(" ")))
            j = 0
            for i, t in enumerate(sent.split(" ")):
                try:
                    j += (1 if doc[i+j].pos_ == "SPACE" else 0)
                    # print(t, doc[i+j].text, doc[i+j].pos_, expl_list[i])
                    pos_dict["pos"].append(doc[i+j].pos_)
                    pos_dict["saliency"].append(expl_list[i])
                    pos_dict["prediction"].append(pred)
                except:
                    print("problem\n")
                    print(sent)
                    try:
                        print(f"i={i}, i+j={i+j}, t={t}, len(doc)={len(doc)}, doc={[(w.text,w.pos_) for w in doc]}")
                    except:
                        print("wrong indexes")
                    print()
            # print(sent)
            # print(pos_dict)
            # print(len(sent.split(" ")))
            # print(len(doc))
            # for w in doc:
            #     print(w.text + ":\t" + w.pos_)
            # print()
            # input()
    df_out = pd.DataFrame.from_dict(pos_dict)
    df_out.to_csv(dest_file,index=False)

# def explain_prediction_2():
    
#     # long_text = request.args.get('text', 0, type=str)
#     long_text = """NEW YORK—In a string of overwhelming and unexpected successes, all of the world’s problems, from hunger to disease to war, were reportedly solved while you slept, with each lingering trace of human suffering having been eliminated by the time you awoke Friday. According to sources, as you lay quietly dreaming in bed, experts from every nation on earth worked tirelessly to end the many crises plaguing society, among them global poverty, ethnic strife, the climate catastrophe, bigotry, and all forms of systemic inequity. Reports confirmed that it was not only matters of urgent, universal importance that were addressed during the seven hours in which you slept but also the slight inconveniences and daily headaches endured by the world’s 7.9 billion people: Potholes were filled in, slow internet connections were sped up, commutes were shortened, and small misunderstanding between neighbors were completely sorted out. Sources went on to report that, due a minor oversight that also occurred as you slumbered, your student loans must still be repaid in full and are now subject to a highly predatory ballooning interest rate."""
    
#     print("prediction for text:", long_text)
#     print("Explaining prediction for text: ", long_text)
    
#     text = preprocess_text(long_text)
#     token_importance_norm_, token_words_ = long_text_prediction_explainability(text)
#     max_exp = np.max(token_importance_norm_)
#     min_exp = np.min(token_importance_norm_)
    
#     # print(max_exp)
    
#     s = (token_importance_norm_ - min_exp) / (max_exp - min_exp+0.01)
#     new_x = s.tolist() 
#     with open("./explainability.txt","w") as f:
#         f.write(str(s[0].tolist()))
#     print(text)
    
#     prediction_, probabilities = satire_prediction(text, 'long_text', None)
    
#     result = {'text':long_text,'tokenization':token_words_,'explanation':new_x,'prediction': prediction_}
    
#     return result

# def eng_conf_mat(df1,df2):

#     lab = ["NOT_SATIRE","SATIRE"]
#     cm = [[954,126],[18,5397]]
#     # df_cm1 = pd.DataFrame(cm1, range(2), range(2))
#     plt.figure(figsize=(10,7))
#     sn.set(font_scale=1.4) # for label size
#     sn.heatmap(cm, annot=True, fmt="",annot_kws={"size": 16},xticklabels = lab,yticklabels=lab) 
#     plt.title("Classifier confusion matrix")# font size
#     plt.show()
#     plt.savefig("./eng_cm.png")

def preprocess_text(sentence):
    import re, html
    sentence = sentence.replace('\n',' ' ) #cleaning newline “\n” from the tweets
    sentence = re.sub(r'(@\S+)|[^\w\s]|#|http\S+', '', sentence)
    sentence = html.unescape(sentence)
    return sentence

# def test_set_evaluation(tweet_sat,tweet_not_sat):
#     from sklearn.metrics import confusion_matrix
#     import seaborn as sn
#     import matplotlib.pyplot as plt
#     from ktrain import load_predictor
#     from tqdm import tqdm
#     BASE_DIR_WEIGHTS = '/mnt/g/.shortcut-targets-by-id/1SowylFaTfsAuRHKJRN7yE6AaIKIojvuz/ThesisMaterial/APP/'
#     predictor = load_predictor(BASE_DIR_WEIGHTS+'weights/Model-for-pred')
#     to_be_predicted = tweet_sat['Text']
#     prob = []
#     y_true = []
#     y_pred = []
#     print(to_be_predicted.shape)
#     for text_ in tqdm(to_be_predicted):
#         text_ = preprocess_text(text_)
#         y_true = y_true + ['SATIRE']
#         if (predictor.predict(text_) == 'SATIRE'):
#             y_pred = y_pred + ['SATIRE']
#         elif (predictor.predict(text_) == 'NOT_SATIRE'):
#             y_pred = y_pred + ['NOT_SATIRE'] 
#     to_be_predicted = tweet_not_sat['Text']
#     for text_ in tqdm(to_be_predicted):
#         y_true = y_true + ['NOT_SATIRE']
#         if (predictor.predict(text_) == 'NOT_SATIRE'):
#             y_pred = y_pred + ['NOT_SATIRE']
#         elif (predictor.predict(text_) == 'SATIRE'):
#             y_pred = y_pred + ['SATIRE']

#     cm = confusion_matrix(y_true, y_pred, labels = ["NOT_SATIRE", "SATIRE"])
#     df_cm1 = pd.DataFrame(cm, range(2), range(2))
#     df_cm1.to_csv("./cm_eng.csv")
#     try:
#         plt.figure(figsize=(10,7))
#         lab = ["NOT_SATIRE","SATIRE"]
#         sn.set(font_scale=1.4) # for label size
#         sn.heatmap(df_cm1, annot=True, fmt="", annot_kws={"size": 16},xticklabels=lab,yticklabels=lab) # font size
#         plt.title("Classifier confusion matrix")
#         plt.savefig("./cm_eng.png")
#         plt.show()
#     except:
#         print("Pippo")

if __name__ == "__main__":
    import pandas as pd
    input_file = "/mnt/g/.shortcut-targets-by-id/1SowylFaTfsAuRHKJRN7yE6AaIKIojvuz/ThesisMaterial/tweet_scraping/Kotiomkin.csv"
    # input_file = "./examples/twittiro.csv"
    dest_file = "./csv/pos_saliency_kot.csv"
    # # manual_labeling(input_file, dest_file)
    df = pd.read_csv(input_file)
    print("Predicting for ", input_file)
    most_relevant_pos(df,dest_file)
    # explain_prediction_2()
    # add1 = "/mnt/g/.shortcut-targets-by-id/1SowylFaTfsAuRHKJRN7yE6AaIKIojvuz/ThesisMaterial/tweet_scraping/thedailymash.csv"
    # add2 = "/mnt/g/.shortcut-targets-by-id/1SowylFaTfsAuRHKJRN7yE6AaIKIojvuz/ThesisMaterial/tweet_scraping/HuffPost.csv"
    # df1, df2 = pd.read_csv(add1).iloc[:1000], pd.read_csv(add2).iloc[:1000]
    # print(df1.shape,df2.shape)
    # test_set_evaluation(df1,df2)