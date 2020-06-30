import re
import sys
import json
import dateparser
from bs4 import BeautifulSoup

months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 
'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
days = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

def clean_brexit(fname):
    ind = 0
    f_out = open('clean/' + fname, 'w')
    with open('timelines/' + fname, 'r') as fp:
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
    f_out = open('clean/' + fname, 'w')
    with open('timelines/' + fname, 'r') as fp: 
        for line in fp:
            if line[0].isdigit():
                content = line.split(" : ")
                curr_date = str(dateparser.parse(content[0]).date())
                if ind != 0 : f_out.write('--------------------------------' + '\n')
                text = '. '.join((line.split(' : ')[1:]))
                f_out.write(curr_date + '\n' + text)
            ind += 1
    f_out.write('\n' + '--------------------------------')
    f_out.close()

def clean_greece(fname):
    ind = 0
    f_out = open('clean/' + fname.split('.')[0] + '.txt', 'w')
    with open('timelines/' + fname) as f:
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
    f_out = open('clean/' + fname, 'w')
    with open('timelines/' + fname, 'r') as fp: 
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

def clean_libya(fname):
    ind = 0
    month_year = ''
    f_out = open('clean/' + fname, 'w')
    with open('timelines/' + fname, 'r') as fp: 
        for line in fp:
            content = line.split(' ')
            if content[0].lower() in months:
                month_year = line.strip('\n')
            elif content[0].lower() in days:
                full_date = content[1] + ' ' + month_year
                curr_date = str(dateparser.parse(full_date).date()) 
                if ind != 0: f_out.write('--------------------------------' + '\n')
                text = '. '.join((line.split('. ')[1:]))
                f_out.write(curr_date + '\n' + text)
                ind += 1
    f_out.write('--------------------------------')
    f_out.close()          

def clean_iraq(fname):
    ind = 0
    curr_year = ''
    curr_month = ''
    f_out = open('clean/' + fname, 'w')
    with open('timelines/' + fname, 'r') as fp: 
        for line in fp:
            if line.startswith('20') and len(line.strip(' \n')) == 4:
                curr_year = line.strip(' \n')
                
            elif line.strip('\n').lower() in months:
                curr_month = line.strip('\n')
                
            elif line[0].isdigit():
                day = line.split(': ')[0]
                full_date = ''
                if len(day.split(' ')) == 1:
                    full_date = day + ' ' + curr_month + ' ' + curr_year
                else:
                    full_date = day + ' ' + curr_year
                curr_date = str(dateparser.parse(full_date).date()) 
                if ind != 0: f_out.write('--------------------------------' + '\n')
                text = '. '.join((line.split(': ')[1:]))
                f_out.write(curr_date + '\n' + text)
                ind += 1
            elif line!='\n': f_out.write(line)
    f_out.write('\n' + '--------------------------------')
    f_out.close()

def clean_syria(fname):
    ind = 0
    f_out = open('clean/' + fname, 'w')
    with open('timelines/' + fname, 'r') as fp: 
        curr_year = ''
        for line in fp:
            if line[0].isdigit():
                curr_year = line.strip('\n')
            elif line!='\n':
                content = line.split(' : ')
                d = content[0].strip('- ')
                curr_date = str(dateparser.parse(d + ' ' + curr_year).date())
                if ind != 0 : f_out.write('--------------------------------' + '\n')
                f_out.write(curr_date + '\n' + content[1])
                ind += 1
    f_out.write('\n' + '--------------------------------')
    f_out.close()

clean_ukraine(sys.argv[1])