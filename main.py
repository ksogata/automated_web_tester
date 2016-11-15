import os
import subprocess
from get_css import asdf

def main():
    subprocess.call(['linkchecker', '--check-extern', 'http://poeresistancecalculator.com', '-Ftext', '-r1'])
    asdf()

if __name__ == '__main__':
    main()
