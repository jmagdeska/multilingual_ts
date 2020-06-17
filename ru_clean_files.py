import sys
import dateparser

def clean(fname):
    ind = 0
    f_out = open('ru_clean/' + fname, 'w')
    with open('ru_timelines/' + fname, 'r') as fp: 
        for line in fp:
            if line[0].isdigit():
                content = line.split(" : ")
                curr_date = str(dateparser.parse(content[0]).date())
                if ind != 0 : f_out.write('--------------------------------' + '\n')
                f_out.write(curr_date + '\n' + content[1])
            elif line != '\n':
                f_out.write(line)
            ind += 1
    f_out.write('\n' + '--------------------------------')
    f_out.close()

def clean_syria(fname):
    ind = 0
    curr_year = ''
    f_out = open('ru_clean/' + fname, 'w')
    with open('ru_timelines/' + fname, 'r') as fp: 
        for line in fp:
            content = line.split(' ')
            if content[0] == '2011' or content[0] == '2012':
                curr_year = content[0]
            elif line != '\n':
                d = content[0] + ' ' + content[1] + ' ' + curr_year
                curr_date = str(dateparser.parse(d).date())
                text = ' '.join(content[2:])
                if ind != 0 : f_out.write('--------------------------------' + '\n')
                f_out.write(curr_date + '\n' + text)
                ind += 1
    f_out.write('\n' + '--------------------------------')
    f_out.close()

clean_syria(sys.argv[1])