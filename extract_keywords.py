import sys
import spacy
from string import punctuation
from collections import Counter
from textacy.ke.textrank import textrank
from spacy.lang.es.stop_words import STOP_WORDS

nlp = spacy.load('es_core_news_sm')

def get_text_rank(doc):
    res = []
    text_rank = textrank(doc, normalize='lower', window_size=2, topn=5)

    for text in text_rank:
        res.append(text[0])
    return res

def get_top_words(doc): 
    res = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN']
    for token in doc:
        if(token.lemma_ in nlp.Defaults.stop_words or token.text in punc or token.text.isdigit()):
            continue
        if(token.pos_ in pos_tag):
            res.append(token.lemma_.lower())

    top5 = [x[0] for x in Counter(res).most_common(5)]
    return top5

f_in = open('es_clean/' + sys.argv[1], 'r')
f_out = open('es_keywords/top_kw_' + sys.argv[1], 'w')
punc = set(punctuation + '“' + '”')

doc = nlp(f_in.read())
keywords = get_top_words(doc)
f_out.write(','.join(keywords))

f_in.close()
f_out.close()