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

clean(sys.argv[1])