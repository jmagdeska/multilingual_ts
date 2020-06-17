import sys
import nltk
nltk.download("stopwords")

import numpy as np
import pandas as pd
from pymystem3 import Mystem
from string import punctuation
from collections import Counter
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

mystem = Mystem() 
russian_sw = stopwords.words("russian")

def preprocess_file(fname):
    text = ''
    with open('ru_clean/' + fname, 'r') as fp: 
        for line in fp:
            if not line.startswith('-') and not line[0].isdigit():
                text += ' ' + line
    return text

def extract_kw(t):
    tokens = mystem.lemmatize(t.lower())
    tokens = [token for token in tokens if token not in russian_sw\
            and token != " " \
            and token.strip() not in punctuation]
    
    cv = CountVectorizer(ngram_range=(1, 2), stop_words=russian_sw, analyzer='word')
    X = cv.fit_transform(tokens)
    word_freq = dict(zip(cv.get_feature_names(), np.asarray(X.sum(axis=0)).ravel()))
    word_counter = Counter(word_freq)
    word_counter_df = pd.DataFrame(word_counter.most_common(5), columns = ['word', 'freq'])
    kw = word_counter_df['word'].tolist()
    return kw

t = preprocess_file(sys.argv[1])
kw = extract_kw(t)
f_out = open('ru_keywords/top_kw_' + sys.argv[1], 'w')
f_out.write(','.join(kw))
f_out.close()