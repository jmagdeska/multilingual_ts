import os
import sys
import spacy
import pickle
from nltk import sent_tokenize
from tilse.data import corpora
from py_heideltime import py_heideltime

lang = {'es':'es_core_news_sm', 'fr':'fr_core_news_sm', 'it':'it_core_news_sm'}
heidel_lang = {'es': 'Spanish', 'fr': 'French', 'it': 'Italian', 'ru' : 'Russian'}

def clean_art(l):
    for topic in os.listdir(dir_art):
        dir_top = dir_art + topic + '/'
        for d in os.listdir(dir_top):
            dir_date = dir_top + d + '/'
            for f in os.listdir(dir_date):
                f_out = ''
                with open(dir_date + f, 'r') as fp:                    
                    for line in fp:
                        content = line.split(' ')
                        if line is not '\n' and len(content) > 2:
                            f_out += line.strip() + '\n'

                with open(dir_date + f, 'w+') as fp2:
                    fp2.write(f_out)

def sent_token(l):
    if l != 'ru':
        nlp = spacy.load(lang[l]) 

    for topic in os.listdir(dir_art):
        for date in os.listdir("/".join([dir_art, topic])):
            for filename in os.listdir("/".join([dir_art, topic, date])):
                if '.tokenized' not in filename:
                    f = "/".join([dir_art, topic, date, filename])
                    sentences = ""
                    with open(f, 'r') as fp:
                        for line in fp.readlines():
                            sentences += line
                    
                    splitted_and_tokenized = ""

                    if l != 'ru':
                        doc = nlp(sentences) 
                        for sent in doc.sents:
                            splitted_and_tokenized += " ".join(
                                [tok.text for tok in sent if not tok.text.isspace()]).strip() + "\n"

                    else:
                        for sent in sent_tokenize(sentences):
                            splitted_and_tokenized += sent.strip() + "\n"

                    splitted_and_tokenized = splitted_and_tokenized.strip()
                    tokenized_filename = "/".join([dir_art, topic, date,
                                                        filename]) + ".tokenized"

                    with open(tokenized_filename, "w") as file:
                        file.write(splitted_and_tokenized)

def tag_heideltime(l):
    path_corpus = l + "/corpus/"
    if not os.path.exists(os.path.dirname(path_corpus)):
        os.mkdir(path_corpus)

    for topic in os.listdir(dir_art):
        print("Heideltime tagging for topic:", topic)
        topic_path = "/".join([path_corpus, topic]) + '/'
        if not os.path.exists(os.path.dirname(topic_path)):
            os.mkdir(topic_path)

        for date in os.listdir("/".join([dir_art, topic])):
            for filename in os.listdir("/".join([dir_art, topic, date])):
                if '.tokenized' in filename:
                    f = "/".join([dir_art, topic, date, filename])
                    f_out = "/".join([topic_path, filename.split('.tokenized')[0]])
                    text = ''
                    fsize = os.path.getsize(f)
                    if fsize > 0:
                        with open(f, 'r') as fp: 
                            for line in fp.readlines():
                                text += line + "\n"

                        res = py_heideltime(text, language=heidel_lang[l],  document_type='news')
                        with open(f_out, "w") as file:
                            file.write(str(res[1]))

def build_corpus(l):
    nlp = spacy.load(lang[l]) 
    path_raw = l + '/corpus/'
    path_dumped = l + "/dumped_corpus/"
    if not os.path.exists(os.path.dirname(path_dumped)):
        os.mkdir(path_dumped)

    for topic in os.listdir(path_raw):
        print("Building corpus for topic:", topic)
        corpus = corpora.Corpus.from_folder(path_raw + topic, nlp)

        with open(path_dumped + topic + ".corpus.obj", "wb") as my_file:
            pickle.dump(corpus, my_file)

l = sys.argv[1]
dir_art = l + '/articles/'
# sent_token(l)
tag_heideltime(l)
# build_corpus(l)
