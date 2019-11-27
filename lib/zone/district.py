import requests
from requests.adapters import HTTPAdapter
from lib.spider.base_spider import BaseSpider
# import sys
# sys.path.append('E:\\工作文档\\sublime\\workspace\\fangjia')
# print(sys.path)
from lib.request.headers import *
from lib.zone.city import cities
from lxml import etree

chinese_city_district_dict = dict() #城市代码和中文名映射
chinese_area_dict = dict()			#板块代码和中文名映射
area_dict = dict()					#板块和区映射

def get_districts(city):
	url = "https://{0}.{1}.com/xiaoqu".format(city,"ke")
	headers = create_headers()
	# print(headers)
	# 不能使用代理，否则访问不了xiaoqu这个页面
	response = requests.get(url, timeout=30, headers=headers)
	html = response.content
	root = etree.HTML(html)
	# elements = root.xpath('//div[3]/div[1]/dl[2]/dd/div/div/a')
	elements = root.xpath('//*[@id="beike"]/div[1]/div[3]/div[1]/dl[2]/dd/div/div/a')
	en_names = list()
	ch_names = list()
	for element in elements:
		link = element.attrib['href']
		en_names.append(link.split('/')[-2])
		ch_names.append(element.text)

	# 打印区县英文和中文名列表
	for index, name in enumerate(en_names):
		chinese_city_district_dict[name] = ch_names[index]
		# print(name + ' -> ' + ch_names[index])
	# print(en_names)
	# print(ch_names)
	return en_names


if __name__ == '__main__':
	for key in cities.keys():
		chinese_city_district_dict = dict()
		get_districts(key)
		if len(chinese_city_district_dict.items()) == 0:
			print(key)