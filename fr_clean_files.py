import re
import sys
import json
import dateparser
from bs4 import BeautifulSoup

def clean_brexit(fname):
    ind = 0
    f_out = open('fr_clean/' + fname, 'w')
    with open('fr_timelines/' + fname, 'r') as fp:
        for line in fp:
            if line[0].isdigit():
                content = line.split(" : ")
                curr_date = str(dateparser.parse(content[0]).date())
                if ind != 0 : f_out.write('--------------------------------' + '\n')
                f_out.write(curr_date + '\n')
            elif line != '\n':
                f_out.write(line)
            ind += 1
    f_out.write('\n' + '--------------------------------')
    f_out.close()

def clean_ukraine(fname):
    ind = 0
    f_out = open('fr_clean/' + fname, 'w')
    with open('fr_timelines/' + fname, 'r') as fp: 
        for line in fp:
            if line[0].isdigit():
                content = line.split(" : ")
                curr_date = str(dateparser.parse(content[0]).date())
                if ind != 0 : f_out.write('--------------------------------' + '\n')
                f_out.write(curr_date + '\n' + content[1])
            ind += 1
    f_out.write('\n' + '--------------------------------')
    f_out.close()

def clean_greece(fname):
    ind = 0
    f_out = open('fr_clean/' + fname.split('.')[0] + '.txt', 'w')
    with open('fr_timelines/' + fname) as f:
        content = json.load(f)
        data = content['data']
        for d in data:
            year = str(d['Année'])
            date = d['Date']
            if date[0].isdigit():
                curr_date = str(dateparser.parse(date + ' ' + year).date())
                if ind != 0: f_out.write('--------------------------------' + '\n')
                cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
                cleantext = re.sub(cleanr, '', d['Para'])
                f_out.write(curr_date + '\n' + cleantext + '\n')
            ind += 1
    f_out.write('--------------------------------')
    f_out.close()

def clean_ukraine2(fname):
    ind = 0
    f_out = open('fr_clean/' + fname, 'w')
    with open('fr_timelines/' + fname, 'r') as fp: 
        soup = BeautifulSoup(fp, 'lxml')
        divs = soup.findAll("div", {"class": "tl-slide"})
        for div in divs:
            d = str(div.find("h3", {"class" : "tl-headline-date"}))
            date = re.search('<h3 class="tl-headline-date">(.*)</h3>', d)[1]
            if '<span' in date:
                date = re.search('<small>(.*)</small>', d)[1]            
            if '-' in date:
                date = date.split(' -')[0]
            curr_date = str(dateparser.parse(date).date()) 
            
            t = str(div.find("p"))
            text = re.search('<p>(.*)</p>', t)[1]
            if ind != 0: f_out.write('--------------------------------' + '\n')
            f_out.write(curr_date + '\n' + text + '\n')
            ind += 1
    f_out.write('--------------------------------')
    f_out.close()

clean_ukraine2(sys.argv[1])