# -*- coding:utf-8 -*-

from requests import post
import json
import time
from json import loads
from os import rename
from os import makedirs
from os.path import exists
from contextlib import closing


def crawler_one_page_data(pageId):
    url = 'https://www.hzyhhr.cn:11443/zpgl/webApi/getAllCmsInfo'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    data = {
        "channelId": 2,
        "pageIndex": pageId,
        "pageSize": 10
    }
    # respond = post(url, headers=headers, data=json.dumps(data))
    respond = post(url, data=data)
    print(respond.content)
    responseJson = json.loads(respond.content)
    print(responseJson)
    print(responseJson['message'])
    return responseJson

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

    all_data = 'id,lxmc,title,summary,source,showdate,publishdate,level,name,sex,birth,company,content\r\n'
    for i in range(0,172): # 左闭右开的区间
        print(i)
        time.sleep(1)
        response_orin = crawler_one_page_data(i)
        code = response_orin['code']
        if code == '200':
            data_list = response_orin['data']
            for response in data_list:
                all_data += response['id'] + ','
                all_data += response['lxmc'] + ','
                all_data += response['title'] + ','
                all_data += response['summary'] + ','
                all_data += response['source'] + ','
                all_data += response['showdate'] + ','
                all_data += response['publishdate'] + ','
                content = response['content']
                level_pre = content.split('拟认定为')
                content_after = ''
                name = ''
                company = ''
                level = ''
                sex = ''
                birth = ''
                if len(level_pre) > 1:
                    # 处理评级
                    level_pre2 = level_pre[1].split('（')
                    level = level_pre2[0]
                    # 处理主要内容，无关的去掉
                    content_split = content.split('</p><p style="text-indent: 2em; line-height: 2em;"><span style="font-size: 20px;">')
                    content_split2 = content_split[1].split('</span></p><p style="text-indent: 2em; line-height: 1.5em;"><span style="font-size: 20px;"><br/></span></p><p style="text-')
                    content_after = content_split2[0]
                    name_split = content_after.split('（')
                    name = name_split[0]
                    company_split = content_after.split('工作单位：')
                    print(company_split)
                    company_split2 = company_split[1].split('，')
                    company = company_split2[0][:-1]
                    print(company)
                    print(company_split2)
                    if len(company_split2) > 1:
                        sex = company_split2[1]
                        birth_split = company_split2[2].split('出生')
                        birth = birth_split[0]
                else:
                    content_after = content

                all_data += level + ','
                all_data += name + ','
                all_data += sex + ','
                all_data += birth + ','
                all_data += company + ','
                all_data += content_after + ','
                all_data += '\r\n'

    write_file_append('./test.csv', all_data)
