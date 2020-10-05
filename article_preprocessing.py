import os
import sys
import spacy
import shlex
import pickle
import codecs
import subprocess
import _pickle as cPickle
from nltk import sent_tokenize
from tilse.data import corpora

if len(sys.argv) != 2:
    print('Please provide the language {es, fr, it, ru}')
    exit()

lang = sys.argv[1]
inputDocs_path = lang + '/articles/'
path = lang + '/articles'
target_path = lang + '/corpus/'
path_raw = path + '/raw/'
path_dumped = lang + '/dumped_corpus/'
heideltime_directory = "/home/jana_magdeska/heideltime/"

lang_model = {'es':'es_core_news_sm', 'fr':'fr_core_news_sm', 'it':'it_core_news_sm', 'en':'en_core_web_sm'}
heidel_lang = {'es': 'Spanish', 'fr': 'French', 'it': 'Italian', 'ru' : 'Russian', 'en':'English'}

nlp = spacy.load(lang_model[lang]) 
LANGUAGE = heidel_lang[lang]

if not os.path.exists(os.path.dirname(path_raw)):
    os.mkdir(path_raw)
if not os.path.exists(os.path.dirname(path_dumped)):
    os.mkdir(path_dumped)

def clean_art():
    for topic in os.listdir(path):
        dir_top = path + topic + '/'
        for d in os.listdir(dir_top):
            dir_date = dir_top + d + '/'
            for f in os.listdir(dir_date):
                f_out = ''
                with codecs.open(f, "r", encoding="utf-8", errors="ignore") as fp:      
                    for line in fp:
                        content = line.split(' ')
                        if line is not '\n' and len(content) > 2:
                            f_out += line.strip() + '\n'

                with open(dir_date + f, 'w+') as fp2:
                    fp2.write(f_out)

def tokenize(art_dir):
    print (" ---------- TOKENIZE ----------\n")
    for topic in os.listdir(art_dir):
        for date in os.listdir('/'.join([art_dir, topic])):
            for filename in os.listdir('/'.join([art_dir, topic, date])):
                if '.tokenized' not in filename:
                    f = '/'.join([art_dir, topic, date, filename])
                    sentences = ""
                    with codecs.open(f, "r", encoding="utf-8", errors="ignore") as fp:
                        for line in fp.readlines():
                            sentences += line
                    
                    splitted_and_tokenized = ""

                    if lang != 'ru':
                        doc = nlp(sentences) 
                        for sent in doc.sents:
                            splitted_and_tokenized += " ".join(
                                [tok.text for tok in sent if not tok.text.isspace()]).strip() + '\n'

                    else:
                        for sent in sent_tokenize(sentences):
                            splitted_and_tokenized += sent.strip() + '\n'

                    splitted_and_tokenized = splitted_and_tokenized.strip()
                    filename = filename.split(".txt")[0]
                    tokenized_filename = '/'.join([path, topic, date,
                                                        filename]) + '.tokenized'

                    with open(tokenized_filename, 'w', encoding="utf-8") as file:
                        file.write(splitted_and_tokenized)

def tag_heideltime(art_dir):
    apply_heideltime = heideltime_directory + "apply_heideltime.jar"
    heideltime_config = heideltime_directory + "config.props"

    ending = "tokenized"
    counter = 0
    print (" ---------- HEIDELTIME ----------\n")

    for topic in os.listdir(art_dir):
        print('Tagging topic:', topic)
        topic_path = '/'.join([art_dir, topic]) + '/'
        for date in os.listdir(topic_path):
            for filename in os.listdir(topic_path + date):
                if ending in filename:
                    filename_to_process = topic_path + date + "/" + filename
                    filename_to_save = filename_to_process + ".timeml"
                    command = "java" + " -jar " + apply_heideltime + " " + filename_to_process + " -l " + LANGUAGE + " -dct " + str(date) + " -t NEWS " + " -c " + heideltime_config + " > " +  filename_to_save             
                    
                    os.popen(command)

    # fix some heideltime bugs
    replace_pairs = [
        ("T24", "T12"),
        (")TMO", "TMO"),
        (")TAF", "TAF"),
        (")TEV", "TEV"),
        (")TNI", "TNI"),
    ]

    for pair in replace_pairs:
        find_command = "find " + path_raw + " -name '*.timeml' -type f -print0"

        find_output = subprocess.Popen(
            shlex.split(find_command),
            stdout=subprocess.PIPE
        )

        sed_command = "xargs -0 sed -i 's/" + pair[0] + "/" + pair[1] + "/g'"

        subprocess.Popen(
            shlex.split(sed_command),
            stdin=find_output.stdout
        )

        find_output.wait()

def build_corpus(art_dir):
    print (" ---------- BUILD CORPUS ----------\n")
    for topic in os.listdir(art_dir):
        if topic != 'raw':
            print('Building corpus for topic:', topic)
            corpus = corpora.Corpus.from_folder(art_dir + '/' + topic, nlp)

            with open(path_dumped + topic + '.corpus.obj', 'wb') as my_file:
                pickle.dump(corpus, my_file)

def dated_sents():
    path_dumped = lang + '/dumped_corpus/'
    target_path = lang + '/dated_sents/'
    if not os.path.exists(os.path.dirname(target_path)):
        os.mkdir(target_path)
    topic_dt_sents = {}
    dated_sentences = {}
    print (" ---------- DATED SENTS ----------\n")

    for corp in os.listdir(path_dumped):
        topic = corp.split('.')[0]
        print('Current topic:', topic)
        dated_sentences[topic] = []
        corpus = pickle.load(open(path_dumped + topic + '.corpus.obj', 'rb'))
        # filtered_corpus = corpus.filter_by_keywords_contained(keyword_mapping[topic])
        dt_sents = {}
        cnt = 0
        for doc in corpus.docs:
            for sent in doc.sentences:      
                dt = sent.date.strftime('%Y-%m-%d')
                time_span = sent.time_span

                dt_sents.setdefault(dt, [])
                dt_sents[dt].append(str(sent))
                cnt += 1

                list_sent = [(str(doc.publication_date), sent, time_span),(dt, sent, time_span)]
                dated_sentences[topic].append(list_sent)
        
        cPickle.dump(dated_sentences[topic], open(target_path + topic + '.dated_sents', 'wb'))
        topic_dt_sents.setdefault(topic, dt_sents)
    cPickle.dump(topic_dt_sents, open(target_path + 'tilse.filtered_sents', 'wb'))

# tokenize(path)

# handle special tokens for xml
pairs = [("&", "&amp;"), ("<", "\&lt;"), (">", "\&gt;")]
for pair in pairs:
    find_command = "find " + path_raw + " -name '*htm*' -type f -print0"
    sed_command = "xargs -0 sed -i 's/" + pair[0] + "/" + pair[1] + "/g'"
    find_output = subprocess.Popen(shlex.split(find_command), stdout=subprocess.PIPE)
    subprocess.Popen( shlex.split(sed_command), stdin=find_output.stdout )
    find_output.wait()

tag_heideltime(path)
build_corpus(path)
dated_sents()
