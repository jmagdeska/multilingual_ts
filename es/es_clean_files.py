import sys
import dateparser
from datetime import datetime
from dateutil.parser import parse

months = {'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04', 
'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08', 'septiembre': '09', 
'octubre': '10', 'noviembre': '11', 'diciembre': '12'}

def clean_turkey(fp, f_out):
    ind = 0
    for line in fp:
        if line.startswith('-'):
            l = line.split('.- ')
            date = l[0].split(' ')
            day = date[1] if len(date[1]) == 2 else '0'+date[1]
            new_date = date[3] + '-' + months[date[2]] + '-' + day
            if ind != 0:
                f_out.write('--------------------------------' + '\n')             
            f_out.write(new_date + "\n" + l[1])
            ind += 1
        
        elif line != '\n': f_out.write(line)

def clean_syria(fp, f_out):
    ind = 0
    for line in fp:
        if line[0].isdigit():
            l = line.split(': ')
            date = l[0].split(' ')
            day = date[0] if len(date[0]) == 2 else '0'+date[0] 
            new_date = date[2] + '-' + months[date[1]] + '-' + day
            if ind != 0:
                f_out.write('--------------------------------' + '\n')  
            f_out.write(new_date + '\n' + l[1])
            ind += 1
           
        else: f_out.write(line)

def clean_syria2(fp, f_out):
    curr_year = '2018'
    ind = 0
    for line in fp:
        if line[0].isdigit():
            if ind != 0:
                f_out.write('--------------------------------' + '\n')
            date = line.split(' ')
            day = date[0] if len(date[0]) == 2 else '0'+date[0] 
            new_date = curr_year + '-' + months[date[2].strip('\n')] + '-' + day
            f_out.write(new_date + '\n')
        elif line != '\n': f_out.write(line)
        
        ind += 1

def clean_iraq(fp, f_out):
    curr_year = ''
    ind = 0
    for line in fp:
        if line.startswith('200'):
            curr_year = line.replace(':\n', '')
        
        elif line[0].isdigit():
            l = line.split('.- ')
            date = l[0].split(' ')           
            month = [m for k, m in months.items() if k.startswith(date[1])]
            day = date[0] if len(date[0]) == 2 else '0'+date[0]
            new_date = curr_year + '-' + month[0] + '-' + day  
            if ind != 0:
                f_out.write('--------------------------------' + '\n')           
            f_out.write(new_date + '\n' + l[1])
            ind += 1

def clean_lebanon(fp, f_out):
    curr_year = ''
    ind = 0
    for line in fp:
        l = line.split(': ')
        date = l[0].split('/')
        if len(date) == 3:
            curr_year = date[2]
        
        day = date[0] if len(date[0]) == 2 else '0'+date[0] 
        new_date = curr_year + '-' + date[1] + '-' + day
        
        if ind != 0:
            f_out.write('--------------------------------' + '\n')  
        f_out.write(new_date + '\n' + l[1])
        ind += 1

def clean_venezuela(fp, f_out):
    last_date = ''
    for line in fp:        
        divs = line.split('class="tl-headline-date">')
        for i in range(2, len(divs)):
            content = divs[i].split('</h3>')
            d = parse(content[0], fuzzy_with_tokens=True)
            curr_date = str(d[0].date())
            text = content[1].split('<div class="tl-text-content"><p>')
            if len(text) != 1:
                t = text[1].split('</p>')[0]
                if curr_date != last_date:
                    last_date = curr_date
                    if i != 2: f_out.write('--------------------------------' + '\n')
                    f_out.write(str(curr_date) + '\n')

                f_out.write(t + '\n')

def clean_greece(fp, f_out):
    curr_year = ''
    ind = 0
    for line in fp:
        if 'AÑO' in line:
            curr_year = line.split(' ')[1].strip('\n')
        elif line[0].isdigit():
            d = line.split('.')[0] + ' ' + curr_year
            curr_date = str(dateparser.parse(d).date())
            text = '. '.join((line.split('. ')[1:]))
            if ind != 0: f_out.write('--------------------------------' + '\n')
            f_out.write(curr_date + '\n' + text)
            ind += 1

def clean_libya(fp, f_out):
    ind = 0
    for line in fp:
        if line[0].isdigit():
                content = line.split(' : ')
                curr_date = str(dateparser.parse(content[0]).date())
                if ind != 0 : f_out.write('--------------------------------' + '\n')
                f_out.write(curr_date + '\n' + content[1])
        ind += 1

def clean_guantanamo(fp, f_out):
    ind = 0
    for line in fp:
        if line[0].isdigit():
            content = line.split(': ')
            curr_date = datetime.strptime(content[0], '%d/%m/%Y').strftime('%Y-%m-%d')
            if ind != 0 : f_out.write('--------------------------------' + '\n')
            f_out.write(curr_date + '\n' + content[1])
            ind += 1

f_in = open('timelines/' + sys.argv[1], 'r')
f_out = open('clean/' + sys.argv[1], 'w')

fp = f_in.readlines()
clean_guantanamo(fp, f_out)
f_out.write('\n' + '--------------------------------')

f_in.close()
f_out.close()
