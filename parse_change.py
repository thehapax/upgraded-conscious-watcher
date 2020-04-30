import sys
from bs4 import BeautifulSoup
import re

def parse_opml(file):
    file = sys.argv[1]
    handler = open(file).read()
    soup = BeautifulSoup(handler, 'html.parser')

    tables = soup.find_all("table")
    print(tables)
    
    """
    for link in soup.find_all("table"): #, class_='topfivetable'):
        try: 
            print("-------")
            print(link)
        except Exception as e:
            pass
    """    

def read_lines(fname): 
    stripped = ''
    with open(fname) as f:
        content = f.readlines()
        for line in content:
            if re.search('^-', line) or re.search('\@\@', line):
                continue
            elif re.search('^\+\+\+', line):
                result = re.sub('^\+\+\+ \@\t', '', line)
                stripped += result +"\n"
            elif re.search('^\+', line):
                result = re.sub('^\+','', line)
                stripped += result +"\n"
            else:
                stripped += line
                       
    return stripped


if __name__ == "__main__":
# opml parsing
    parsed_lines = read_lines(sys.argv[1])
    print(parsed_lines)
    