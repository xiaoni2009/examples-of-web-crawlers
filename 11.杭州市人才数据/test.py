# -*- coding:utf-8 -*-

from requests import get
import json
import time
from bs4 import BeautifulSoup
from json import loads
from os import rename
from os import makedirs
from os.path import exists
from contextlib import closing



if __name__ == '__main__':
    print('hello world')

    # 找不到会报错
    #a = 'hello'.index('a')
    #print(a)

    b = 'hello'.find('a')
    print(b)
    b = 'hello'.find('l')
    print(b)
    b = 'hello'.find('o')
    print(b)