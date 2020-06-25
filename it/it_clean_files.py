import re
import sys
import dateparser

months = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 
'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']

def clean(fname):
    ind = 0
    f_out = open('clean/' + fname, 'w')
    with open('timelines/' + fname, 'r') as fp:
        for line in fp:
            if line[0].isdigit():
                content = line.split(' : ')
                curr_date = str(dateparser.parse(content[0]).date())
                text = '. '.join((line.split(' : ')[1:]))
                if ind != 0 : f_out.write('--------------------------------' + '\n')
                f_out.write(curr_date + '\n' + text)
            elif line != '\n':
                f_out.write(line)
            ind += 1
    f_out.write('\n' + '--------------------------------')
    f_out.close()

def clean2(fname):
    ind = 0
    curr_date = ''
    curr_year = ''
    f_out = open('clean/' + fname, 'w')
    with open('timelines/' + fname, 'r') as fp:
        for line in fp:
            if line.strip('\n') == '2003' or line.strip('\n') == '2004':
                curr_year = line.strip('\n')
            elif line[0].isdigit():
                content = line.split(' ')
                if len(content) > 2 and content[1] in months:
                    d = line.split(' - ')[0]
                    d += ' ' + curr_year
                    d = str(dateparser.parse(d).date())
                    if d != curr_date:
                        curr_date = d
                        if ind != 0: f_out.write('--------------------------------' + '\n')
                        f_out.write(curr_date + '\n')
                    text = ' '.join((line.split(' - ')[1:]))
                    f_out.write(text)
                ind += 1
            else:
                f_out.write(line)
                ind+=1

    f_out.write('\n' + '--------------------------------')
    f_out.close()

clean2(sys.argv[1])