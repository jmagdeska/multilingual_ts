import sys
import requests
import dateparser
from datetime import datetime, timedelta
from urllib.parse import quote
from GoogleNews import GoogleNews
from dateutil.parser import parse

def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def get_date_range(fp):
    dates = []

    for line in fp:
        if is_date(line):
            date = str(parse(line).date())
            dates.append(date)

    min_d = (datetime.strptime(min(dates), '%Y-%m-%d') - timedelta(days=10)).strftime('%m/%d/%Y')
    max_d = (datetime.strptime(max(dates), '%Y-%m-%d') + timedelta(days=10)).strftime('%m/%d/%Y')
    num_dates = len(dates)

    return min_d, max_d, num_dates

def get_keywords(d,topic):
    f1 = open(d + 'top_kw_' + topic + '.txt', 'r')
    f2 = open(d + 'manual_' + topic + '.txt', 'r')

    top_kw = f1.readline().strip('\n').split(',')
    manual_kw = f2.readline().strip('\n').split(',')
  
    kw = ','.join(list(set(top_kw).union(set(manual_kw))))
    return kw

def extract_links(dir_c, dir_k, lang):
    for t in topics:
        print('Current topic: ', t + '\n')

        kw = get_keywords(dir_k, t)
        print('Keywords: ', kw + '\n')

        f_clean = open(dir_c + t + '.txt', 'r')
        fp = f_clean.readlines()
        min_d, max_d, num_d = get_date_range(fp)
        print('Date range: ', min_d, max_d + '\n')

        f_out = open(lang + '_news/' + t + '_links.txt', 'w')

        key_enc = quote(kw.encode('utf8'))
        googlenews = GoogleNews()
        googlenews.setlang(lang)
        googlenews.setTimeRange(min_d, max_d)
        googlenews.search(key_enc)
        result = googlenews.result()
        page = 1
        num_art = 0
        num_curr = 0

        while len(result) > 0 and num_art < 10*num_d:
            date = str(dateparser.parse(result[num_curr]['date']).date())
            link = result[num_curr]['link']
            f_out.write(date + '\n' + link)
            f_out.write('\n--------------------------------\n')

            num_art += 1
            num_curr += 1

            if num_curr == len(result):
                num_curr = 0
                page += 1
                googlenews.getpage(page)
                result = googlenews.result()

        print('--------------------------------\n')
        f_out.close()

lang = sys.argv[1]
topics = ['iraq', 'lebanon', 'syria']
dir_clean = lang + '_clean/'
dir_kw = lang + '_keywords/'

extract_links(dir_clean, dir_kw, lang)