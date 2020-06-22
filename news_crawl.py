import sys
import requests
import dateparser
from bs4 import BeautifulSoup
from datetime import datetime
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
    min_d = datetime.strptime(min(dates), '%Y-%m-%d').strftime('%m/%d/%Y')
    max_d = datetime.strptime(max(dates), '%Y-%m-%d').strftime('%m/%d/%Y')
    
    return min_d, max_d

def extract_links(dir_c, dir_k, lang):
    for t in topics:
        print('Current topic: ', t + '\n')
        f_kw = open(dir_k + 'top_kw_' + t + '.txt', 'r')
        kw = ','.join(f_kw.readlines()).strip('\n')
        print('Keywords: ', kw + '\n')

        f_clean = open(dir_c + t + '.txt', 'r')
        fp = f_clean.readlines()
        min_d, max_d = get_date_range(fp)
        print('Date range: ', min_d, max_d + '\n')

        f_out = open(lang + '_news/' + t + '_links.txt', 'w')

        googlenews = GoogleNews()
        googlenews.setlang(lang)
        googlenews.setTimeRange(min_d, max_d)
        googlenews.search(kw)
        result = googlenews.result()
        page = 1
        n = 0

        while len(result) > 0 and page < 3:
            date = str(dateparser.parse(result[n]['date']).date())
            link = result[n]['link']
            f_out.write(date + '\n' + link)
            f_out.write('\n--------------------------------\n')

            n += 1
            if n == len(result):
                n = 0
                page += 1
                googlenews.getpage(page)
                result = googlenews.result()

        print('--------------------------------\n')
        f_out.close()

lang = sys.argv[1]
topics = ['iraq', 'lebanon', 'libya', 'syria']
dir_clean = lang + '_clean/'
dir_kw = lang + '_keywords/'

extract_links(dir_clean, dir_kw, lang)