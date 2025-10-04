## List trained models
List of saved models train on different document size (100 doc, 90K number of document on 100 iterations)

- sklearn_crf_model_100-100i.sav -- size: 2.1M
- sklearn_crf_model_90k-100i.sav -- size: 41M

Suggest using 90K for better accuracy.

## How to use the model

crf.py: the main entry point for using a pre-trained Conditional Random Field (CRF) model to perform word segmentation on Khmer text. Its primary role is to load the trained model, process an input sentence, and use the model to predict where word boundaries should be.

