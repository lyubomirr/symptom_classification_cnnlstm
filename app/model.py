import tensorflow as tf
import numpy as np
import nltk
import string
import pickle
import re

from tensorflow import keras
from nltk.stem import WordNetLemmatizer
from spacy.lang.en.stop_words import STOP_WORDS
from tensorflow.keras.preprocessing.sequence import pad_sequences

MAX_SEQUENCE_LENGTH = 30

def _config_memory_growth():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)

_config_memory_growth()    

model = keras.models.load_model("trained_model")
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('labelencoder.pickle', 'rb') as handle:
    label_encoder = pickle.load(handle)

def predict(text):
    processed = preprocess(text)
    predictions = model.predict(pad_sequences(tokenizer.texts_to_sequences([processed]),maxlen=MAX_SEQUENCE_LENGTH))
    predicted_label_num = np.argmax(predictions,axis=-1)

    predicted_label = label_encoder.inverse_transform(predicted_label_num)[0]
    return predicted_label, 100 * np.max(predictions)

def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    
    tokens = nltk.word_tokenize(text)
    lower = [t.lower() for t in tokens]
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    stripped = [re_punc.sub('', w) for w in lower]
    words = [word for word in stripped if word.isalpha()]
    words = [w for w in words if not w in  list(STOP_WORDS)]
    words = [word for word in words if len(word) > 2]
    lem_words = [lemmatizer.lemmatize(word) for word in words]
    return lem_words