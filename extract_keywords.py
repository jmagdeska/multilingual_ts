import sys
import spacy
from string import punctuation
from collections import Counter
from textacy.ke.sgrank import sgrank
from spacy.lang.es.stop_words import STOP_WORDS

def get_text_rank(doc):
    res = []
    text_rank = sgrank(doc, ngrams=(1, 2), normalize='lower', topn=5, include_pos=('PROPN', 'ADJ', 'NOUN'))

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

f_in = open(sys.argv[1] + '_clean/' + sys.argv[2], 'r')
f_out = open(sys.argv[1] + '_keywords/top_kw_' + sys.argv[2], 'w')
punc = set(punctuation + '“' + '”')

nlp = spacy.load('es_core_news_sm') if sys.argv[1] == 'es' else spacy.load('fr_core_news_sm')
doc = nlp(f_in.read())
keywords = get_text_rank(doc)
f_out.write(','.join(keywords))

f_in.close()
f_out.close()