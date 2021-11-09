
from storyteller.secrets import WISDOMS_V0, WISDOMS_V1
import requests
import csv


def main():
    r = requests.get(WISDOMS_V0)
    r.encoding = 'utf-8'
    print(r.text)
    r = requests.get(WISDOMS_V1)
    r.encoding = 'utf-8'
    reader = csv.reader(r.text.split("\n"), delimiter="\t")
    for row in reader:
        print(row[0])


if __name__ == '__main__':
    main()
