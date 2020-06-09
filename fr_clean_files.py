import sys
import dateparser

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
clean_brexit(sys.argv[1])