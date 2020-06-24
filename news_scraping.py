import os
import sys
import requests
from bs4 import BeautifulSoup

def get_articles(l):
    topics = ['iraq', 'lebanon', 'libya', 'syria']
    dir_links = l + '_links/'
    dir_art = l + '_articles/'
    if not os.path.exists(os.path.dirname(dir_art)):
        os.mkdir(dir_art)

    for t in topics:
        if not os.path.exists(os.path.dirname(dir_art + t + '/')):
            os.mkdir(dir_art + t)
        with open(dir_links + t + '_links.txt', 'r') as fp:
            curr_dir = ''
            i = 0
            for line in fp:
                if line[0].isdigit():
                    curr_dir = dir_art + t + '/' + line.strip('\n') + '/'
                    if not os.path.exists(os.path.dirname(curr_dir)):
                        os.mkdir(curr_dir)
                elif line.startswith('http'):
                    url = line.strip('\n')
                    print('Current url: ', url)
                    code = requests.get(url, headers={'Accept-Encoding': 'deflate'}, allow_redirects=False)
                    soup = BeautifulSoup(code.text,'lxml')
                    with open(curr_dir + str(i) + '.txt', 'w', encoding='utf-8') as f_out:
                        for title in soup.find_all('p'):
                            f_out.write(title.text)
                        f_out.close()
                        i += 1

lang = sys.argv[1]
get_articles(lang)

