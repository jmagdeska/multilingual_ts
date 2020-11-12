import os
import sys
import spacy
import shlex
import pickle
import codecs
import subprocess
import _pickle as cPickle
from tilse.data import corpora

if len(sys.argv) != 2:
    print('Please provide the runtime {l, r}')
    exit()

def clean_art():
    for topic in os.listdir(ART_PATH):
        dir_top = ART_PATH + "/" + topic + "/"
        for d in os.listdir(dir_top):
            dir_date = dir_top + d + "/"         
            for f in os.listdir(dir_date):
                f = dir_date + f
                f_out = ''
                with codecs.open(f, "r", encoding="utf-8", errors="ignore") as fp:      
                    for line in fp:
                        content = line.split(' ')
                        if line is not '\n' and len(content) > 2:
                            f_out += line.strip() + '\n'

                with open(f, 'w+') as fp2:
                    fp2.write(f_out)

def tokenize():
    print (" ---------- TOKENIZE ----------\n")
    for topic in os.listdir(ART_PATH):
        for date in os.listdir('/'.join([ART_PATH, topic])):
            for filename in os.listdir('/'.join([ART_PATH, topic, date])):
                if '.tokenized' not in filename:
                    f = '/'.join([ART_PATH, topic, date, filename])
                    sentences = ""
                    with codecs.open(f, "r", encoding="utf-8", errors="ignore") as fp:
                        for line in fp.readlines():
                            sentences += line
                    
                    splitted_and_tokenized = ""

                    if len(sentences) < 1000000:
                        doc = nlp(sentences) 
                        del sentences
                        for sent in doc.sents:
                            splitted_and_tokenized += " ".join(
                                [tok.text for tok in sent if not tok.text.isspace()]).strip() + '\n'
                        
                        del doc
                        splitted_and_tokenized = splitted_and_tokenized.strip()
                        filename = filename.split(".txt")[0]
                        tokenized_filename = '/'.join([ART_PATH, topic, date,
                                                            filename]) + '.tokenized'

                        with open(tokenized_filename, 'w', encoding="utf-8") as file:
                            file.write(splitted_and_tokenized)

def tag_heideltime(topics):
    apply_heideltime = HEIDEL_DIR + "/apply_heideltime.jar"
    heideltime_config = HEIDEL_DIR + "/config.props"

    ending = "tokenized"
    counter = 0
    print (" ---------- HEIDELTIME ----------\n")

    for topic in topics:
        print('Tagging topic:', topic)
        topic_path = '/'.join([ART_PATH, topic]) + '/'
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
        find_command = "find " + RAW_PATH + " -name '*.timeml' -type f -print0"

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

def build_corpus(topics):
    print (" ---------- BUILD CORPUS ----------\n")
    for topic in topics:
        print('Building corpus for topic:', topic)
        corpus = corpora.Corpus.from_folder(ART_PATH + '/' + topic, nlp)

        with open(DUMPED_PATH + topic + '.corpus.obj', 'wb') as my_file:
            pickle.dump(corpus, my_file)

def dated_sents():
    DATED_PATH = ROOT_PATH + "/" + lang + "/dated_sents/"
    if not os.path.exists(os.path.dirname(DATED_PATH)):
        os.mkdir(DATED_PATH)
    topic_dt_sents = {}
    dated_sentences = {}
    print (" ---------- DATED SENTS ----------\n")

    for corp in os.listdir(DUMPED_PATH):
        topic = corp.split('.')[0]
        print('Current topic:', topic)
        dated_sentences[topic] = []
        corpus = pickle.load(open(DUMPED_PATH + "/" + topic + ".corpus.obj", "rb"))
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
                
        cPickle.dump(dated_sentences[topic], open(DATED_PATH + topic + '.dated_sents', 'wb'))
        del dated_sentences[topic]
        topic_dt_sents.setdefault(topic, dt_sents)
    cPickle.dump(topic_dt_sents, open(DATED_PATH + 'tilse.filtered_sents', 'wb'))

local = True if sys.argv[1] == "l" else False
lang_topic = {"es": ["egypt-2", "libya-2", "yemen"], 
        "fr": ["iraq-2", "syria-2", "libya-2", "egypt"],
        "it": ["egypt-2", "libya", "syria-2"]}

ROOT_PATH = "/home/jana/Documents/PoliTo/Thesis/multilingual_ts" if local == True else "/home/jana_magdeska/multilingual_ts"
HEIDEL_DIR = "/home/jana/heideltime" if local == True else "/home/jana_magdeska/heideltime"

lang_model = {'es':'es_core_news_sm', 'fr':'fr_core_news_sm', 'it':'it_core_news_sm', 'ru':'xx_ent_wiki_sm'}
heidel_lang = {'es': 'Spanish', 'fr': 'French', 'it': 'Italian', 'ru' : 'Russian'}

for lang in lang_topic.keys():
    ART_PATH = ROOT_PATH + "/" + lang + "/articles"
    RAW_PATH = ART_PATH + "/raw/"
    DUMPED_PATH = ROOT_PATH + "/" + lang + "/dumped_corpus/"

    nlp = spacy.load(lang_model[lang]) 
    LANGUAGE = heidel_lang[lang]
    if not os.path.exists(os.path.dirname(RAW_PATH)):
        os.mkdir(RAW_PATH)
    if not os.path.exists(os.path.dirname(DUMPED_PATH)):
        os.mkdir(DUMPED_PATH)

    topics = lang_topic[lang] 
    tag_heideltime(topics)
    build_corpus(topics)
    dated_sents()

# if lang == 'ru':
#     nlp.add_pipe(nlp.create_pipe('sentencizer'))

# clean_art()
# tokenize()

# handle special tokens for xml
# pairs = [("&", "&amp;"), ("<", "\&lt;"), (">", "\&gt;")]
# for pair in pairs:
#     find_command = "find " + RAW_PATH + " -name '*htm*' -type f -print0"
#     sed_command = "xargs -0 sed -i 's/" + pair[0] + "/" + pair[1] + "/g'"
#     find_output = subprocess.Popen(shlex.split(find_command), stdout=subprocess.PIPE)
#     subprocess.Popen( shlex.split(sed_command), stdin=find_output.stdout )
#     find_output.wait()
