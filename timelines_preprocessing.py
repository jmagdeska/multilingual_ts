import os
import re
import sys
import spacy
import codecs

lang = sys.argv[1]
gt_dir = lang + '/clean/'

lang_model = {'es':'es_core_news_sm', 'fr':'fr_core_news_sm', 'it':'it_core_news_sm', 'ru':'xx_ent_wiki_sm'}
nlp = spacy.load(lang_model[lang]) 

if lang == 'ru':
    nlp.add_pipe(nlp.create_pipe('sentencizer'))

def sent_tokenize(sentences):
    splitted_and_tokenized = ""

    doc = nlp(sentences) 
    for sent in doc.sents:
        splitted_and_tokenized += " ".join(
            [tok.text for tok in sent if not tok.text.isspace()]).strip() + '\n'

    splitted_and_tokenized = splitted_and_tokenized.strip()
    return splitted_and_tokenized

print (" ---------- TIMELINE TOKENIZE ----------\n")
for f in os.listdir(gt_dir):
    sentences = ""
    f_out = ""
    filename = gt_dir + f
    
    with codecs.open(filename, "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp.readlines():
            if line[0].isdigit() or line == '--------------------------------':
                f_out += line
            else:
                tokenized = sent_tokenize(line)
                f_out += tokenized + '\n'
    
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(f_out)
