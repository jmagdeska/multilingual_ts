import re
import sys
import dateparser

def clean(fname):
    ind = 0
    f_out = open('it_clean/' + fname, 'w')
    with open('it_timelines/' + fname, 'r') as fp:
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

clean(sys.argv[1])