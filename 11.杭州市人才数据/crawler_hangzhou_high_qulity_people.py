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


def crawler_one_page_data(pageId):
    url = 'https://rc.hzrs.hangzhou.gov.cn/articles/detail/' + pageId.__str__() + '.html'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    respond = get(url, headers=headers)
    # print(respond.content)
    # responseJson = json.loads(respond.content)
    # print(responseJson)
    # print(responseJson['message'])
    return BeautifulSoup(respond.content,'lxml')

def read_file(path):
    f = open(path)
    data = f.read()
    f.close()
    return data

# 追加写文件
def write_file_append(path, data):
    f = open(path, 'a')
    f.write(data)
    f.close()

if __name__ == '__main__':
    print('hello world')

    title_data = 'pageId,title,publish_date,publisher,area,level,name,sex,birth,company,content\r\n'
    write_file_append('./test.csv', title_data)
    # 20210402 pageId到39502闭区间
    for i in range(13,39503): # 左闭右开的区间
        print(i)
        time.sleep(0.3)
        try:
            response_orin = crawler_one_page_data(i)
            # print(response_orin)
            title_tag = response_orin.find('title')
            # print(title_tag)
            if title_tag is not None:
                title = title_tag.string
                print(title)
                if title is not None and title.find('认定为高层次人才的公示') >= 0:
                    print('123')
                    main_body = response_orin.find(attrs={'class':'main'})
                    pp = main_body.findAll(name='p')[:2]
                    p0 = pp[0]
                    p0_str = p0.string
                    # print(p0_str)
                    p0_str_split = p0_str.split('发布日期:')
                    # print(p0_str_split)
                    publish_date = p0_str_split[1][:10]
                    # print(publish_date)
                    publisher = p0_str_split[0].split('作者：')[1]
                    print(publisher)
                    p1 = pp[1]
                    span_all = p1.findAll(name='span')
                    # print(span_all)
                    name = span_all[0].string
                    company = span_all[1].string
                    print(name)
                    print(company)
                    level = span_all[2].string
                    print(level)
                    p1_str = str(p1)
                    sex_birth_split = p1_str.split('，')
                    # print(sex_birth_split)
                    sex = sex_birth_split[1]
                    birth = sex_birth_split[2][:-2]
                    print(sex)
                    print(birth)
                    content_str = p1_str.replace('\r\n','').replace('\r','').replace('\n','')
                    area_split = sex_birth_split[0].split('所属部门：')
                    area = ''
                    if len(area_split) > 1:
                        area = area_split[1].split('；')[0]
                        print(area)

                    all_data = str(i) + ','
                    all_data += title.strip() + ','
                    all_data += publish_date.strip() + ','
                    all_data += publisher.strip() + ','
                    all_data += area.strip() + ','
                    all_data += level.strip() + ','
                    all_data += name.strip() + ','
                    all_data += sex.strip() + ','
                    all_data += birth.strip() + ','
                    all_data += company.strip() + ','
                    all_data += content_str.strip()
                    all_data += '\r\n'

                    write_file_append('./test.csv', all_data)
        except:
            print(str(i) + ' error')
