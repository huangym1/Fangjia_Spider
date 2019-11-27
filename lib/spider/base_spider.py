
import random
import sys
import threading
import requests
from requests.adapters import HTTPAdapter
from lib.utility.date import  *
sys.path.append('E:\\工作文档\\sublime\\workspace\\fangjia')
from lib.zone.city import lianjia_cities,beike_cities
from lib.item.ershou import *
from pymongo import MongoClient

LIANJIA_SPIDER = "lianjia"
BEIKE_SPIDER = "ke"
# SPIDER_NAME = LIANJIA_SPIDER
SPIDER_NAME = BEIKE_SPIDER
thread_pool_size = 5


class BaseSpider(object):
	def __init__(self):
		self.mutex = threading.Lock()
		self.date_string = get_date_string()
		self.total_num = 0 # 统计小区个数
		self.nodata_list = list() #统计哪些板块没有数据
		self.chinese_nodata_list = list()
		self.title = ErShou.title(self)
		self.html = None
		try:
			self.conn = MongoClient('192.168.6.128', 28013)
			self.db = self.conn.fangjia
			self.my_set = self.db.ershoufang
		except Exception as e:
			print(e)

	def get_proxy(self):
		# self.ip_pool_db = self.conn.proxy
		# self.ip_pool_set = self.ip_pool_db.useful_proxy
		# return self.ip_pool_set.find()[0]['proxy']
		return requests.get("http://192.168.6.128:5010/get/").text

	def delete_proxy(self,proxy):
		return requests.get("http://192.168.6.128:5010/delete/?proxy={}".format(proxy))

	def proxy_request(self,url,headers):
		# 新的方法
		proxy = BaseSpider().get_proxy()
		s = requests.session()
		s.mount("http://", HTTPAdapter(max_retries=3))
		s.mount("https://", HTTPAdapter(max_retries=3))
		try:
			self.html = s.get(url, timeout=20, headers=headers, \
								proxies={"http": "http://{}".format(proxy)}).text
		except Exception as e:
			print(e)
		return self.html

if __name__ == '__main__':
	B = BaseSpider()
	print(B.title)




