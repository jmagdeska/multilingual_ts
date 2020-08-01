import os
import sys
import spacy
# from python-heideltime import HeidelTime

lang = {'es':'es_core_news_sm', 'fr':'fr_core_news_sm', 'it':'it_core_news_sm'}
heidel_lang = {'es': 'spanish', 'fr': 'french', 'it': 'italian'}

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

def build_corpus(l):
    nlp = spacy.load(lang[l]) 

    for topic in os.listdir(dir_art):
        if topic == 'yemen':
            for date in os.listdir("/".join([dir_art, topic])):
                for filename in os.listdir("/".join([dir_art, topic, date])):
                    if '.tokenized' not in filename:
                        print(filename)
                        f = "/".join([dir_art, topic, date, filename])
                        sentences = ""
                        with open(f, 'r') as fp:
                            for line in fp.readlines():
                                sentences += line
                        
                        doc = nlp(sentences)
                        splitted_and_tokenized = ""

                        for sent in doc.sents:
                            splitted_and_tokenized += " ".join(
                                [tok.text for tok in sent if not tok.text.isspace()]).strip() + "\n"

                        splitted_and_tokenized = splitted_and_tokenized.strip()

                        tokenized_filename = "/".join([dir_art, topic, date,
                                                        filename]) + ".tokenized"

                        with open(tokenized_filename, "w") as file:
                            file.write(splitted_and_tokenized)

# def tag_heideltime():
#     ht = HeidelTime.HeidelTimeWrapper(heidel_lang[l])
#     ht_sents = ''
#     with open(dir_art + 'egypt' + '2011-01-31/14.txt.tokenized', 'r') as fp:
#         for line in fp:
#             heidel = ht.parse(line)
#             print(heidel)

l = sys.argv[1]
dir_art = l + '/articles/'
build_corpus(l)