# -*- coding: utf-8 -*-

def file2list(text_file):
    try:
        f = open(text_file)
    except IOError:
        print('file %s not exist' %text_file)
        exit(1)
        #return 1

    for i in f.read().splitlines():
        print(i)
"""

"""

"""

# file2list('config.txt')

"""
        mas_text = []
        for line in f.readlines():
            if line == "Hostname\n":
                return mas_text
            mas_text.append(line)
                f.close()

"""


