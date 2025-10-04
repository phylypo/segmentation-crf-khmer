### first install sklearn_crfsuite
# pip install sklearn_crfsuite

# import of the crf library
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

import pickle
from crf_lib import *

file = './sklearn_crf_model_90k-100i.sav'
# load the model from disk
loaded_model = pickle.load(open(file, 'rb'))

# Create KCC using phrase, but pass in the whole sentence to CRF
def segment_kcc_phrase(sentence):
  complete = ""
  sentence = sentence.replace(u'\u200b','')
  for ph in sentence.split():
    kccs = seg_kcc(ph)

    features = create_kcc_features(kccs)
    prediction = loaded_model.predict([features])
    for i, p in enumerate(prediction[0]):
        if p == "1":
            complete += " " + kccs[i]
        else:
            complete += kccs[i]
    complete += " "
  complete=complete.strip()
  return complete

#testing call
'''
t = "ចំណែកជើងទី២២២២ នឹងត្រូវធ្វើឡើងឯប្រទេសកាតា៕\nពួកគាត់តវ៉ាប្ដឹងទៅមេឃុំចៅវ៉ាយស្រុកជាច្រើនលើកដែរ ។"
t_correct = "ចំណែក ជើង ទី ២២២២ នឹង ត្រូវ ធ្វើឡើង ឯ ប្រទេស កាតា ៕\nពួកគាត់ ត វ៉ាប្ដឹង ទៅ មេឃុំ ចៅវ៉ាយ ស្រុក ជាច្រើន លើក ដែរ ។ "
skcc = seg_kcc(t)
print("len kcc:", len(skcc), skcc)
features = create_kcc_features(skcc)
features = [features]
print("features:", features)
print("\npredict seg:", loaded_model.predict(features))
print("\nseg:", segment_kcc_phrase(t))
'''

def cleanup_str(str):
  #str = correct_str(str)
  # remove special characters
  str = str.replace(u"\u2028", "") # line separator
  str = str.replace(u"\u200a", "")  # hair space
  str = str.replace("<br>"," ") # changed to space
  return str.strip().replace('\n',' ').replace('  ',' ')

def crf_segment(t):
  t = cleanup_str(t)
  kccs = seg_kcc(t)
  features = create_kcc_features(kccs)
  features = [features]
  return segment_kcc_phrase(t)

## call crf segment using
t='my text abc'
t = "ចំណែកជើងទី២២២២ នឹងត្រូវធ្វើឡើងឯប្រទេសកាតា៕\nពួកគាត់តវ៉ាប្ដឹងទៅមេឃុំចៅវ៉ាយស្រុកជាច្រើនលើកដែរ ។"
t_correct = "ចំណែក ជើង ទី ២២២២ នឹង ត្រូវ ធ្វើឡើង ឯ ប្រទេស កាតា ៕ ពួកគាត់ តវ៉ា ប្ដឹង ទៅ មេឃុំ ចៅវ៉ាយ ស្រុក ជាច្រើន លើក ដែរ ។"
newtext = crf_segment(t)
print("new text:", newtext)
print("correct :", t_correct)