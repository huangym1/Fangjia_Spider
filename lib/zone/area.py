import requests
import sys
sys.path.append('E:\\工作文档\\sublime\\workspace\\fangjia')
# print(sys.path)
from lib.request.headers import *
from lib.zone.district import *
from lib.zone.city import cities
from lxml import etree
from requests.adapters import HTTPAdapter
from lib.spider.base_spider import BaseSpider

def get_areas(city,district):
	page = "http://{0}.{1}.com/xiaoqu/{2}".format(city, 'ke', district)
	areas = list()
	try:
		headers = create_headers()
		# 不能使用代理，否则访问不了xiaoqu这个页面
		responses = requests.get(page, timeout=30, headers=headers)
		html = responses.content
		# print(response)
		root = etree.HTML(html)
		elements = root.xpath('//*[@id="beike"]/div[1]/div[3]/div[1]/dl[2]/dd/div/div[2]/a')
		en_names = list()
		cn_names = list()
		for element in elements:
			link = element.attrib['href']
			# en_names.append(link[:-1].split("/")[-1])
			en_names.append(link.split('/')[-2])
			cn_names.append(element.text)

		for index,name in enumerate(en_names):
			chinese_area_dict[name] = cn_names[index]

		# print("dict is :{0}".format(chinese_area_dict))
		return en_names

	except Exception as e:
		print(e)

# def get_areas(city,district):
#     page = get_district_url(city, district)
#     areas = list()
#     try:
#         headers = create_headers()
#         response = requests.get(page, timeout=10, headers=headers)
#         html = response.content
#         root = etree.HTML(html)
#         links = root.xpath('//div[3]/div[1]/dl[2]/dd/div/div[2]/a')

#         # 针对a标签的list进行处理
#         for link in links:
#             relative_link = link.attrib['href']
#             # 去掉最后的"/"
#             relative_link = relative_link[:-1]
#             # 获取最后一节
#             area = relative_link.split("/")[-1]
#             # 去掉区县名,防止重复
#             if area != district:
#                 chinese_area = link.text
#                 chinese_area_dict[area] = chinese_area
#                 # print(chinese_area)
#                 areas.append(area)
#         return areas
#     except Exception as e:
#         print(e)



if __name__ == "__main__":
	print(get_areas("gz", "panyu"))
    