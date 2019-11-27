#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 城市缩写和城市名的映射
# 想抓取其他已有城市的话，需要把相关城市信息放入下面的字典中
# 不过暂时只有下面这些城市在链家上是统一样式

import sys
# from lib.utility.version import PYTHON_3
# from lib.utility.log import *

cities = {
    'bj': '北京',
    'cd': '成都',
    'cq': '重庆',
    'cs': '长沙',
    'dg': '东莞',
    'dl': '大连',
    'fs': '佛山',
    'gz': '广州',
    'hz': '杭州',
    'hf': '合肥',
    'jn': '济南',
    'nj': '南京',
    'qd': '青岛',
    'sh': '上海',
    'sz': '深圳',
    'su': '苏州',
    'sy': '沈阳',
    'tj': '天津',
    'wh': '武汉',
    'xm': '厦门',
    'yt': '烟台',
}


lianjia_cities = cities
beike_cities = cities


def get_city():
    prompt = create_prompt_text()
    city = input(prompt)
    chinese_city = get_chinese_city(city)
    message = "开始爬取.. " + chinese_city
    print(message)
    return city


def get_chinese_city(en):
    return cities.get(en)

def create_prompt_text():
    city_info = list()
    count = 0
    for en_name,cn_name in cities.items():
        count += 1
        city_info.append(en_name)
        city_info.append(": ")
        city_info.append(cn_name)
        if count % 4 == 0:
            city_info.append('\n')
        else:
            city_info.append(',')
    return ''.join(city_info)

if __name__ == '__main__':
    get_city()