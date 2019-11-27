
# import sys
# sys.path.append('E:\\工作文档\\sublime\\workspace\\fangjia')
import requests
import re
import threadpool
from lib.spider.base_spider import *
from lib.zone.city import get_city
from lib.zone.area import *
from lib.request.headers import *
from lib.utility.path import *
from lib.utility.date import *
from lib.zone.district import get_districts
from lib.zone.area import get_areas
from lib.item.zufang import *
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

class  ZuFangBaseSpider(BaseSpider):
	"""docstring for  ZuFangBaseSpider"""
	def collect_area_zufang_info(self,city_name,area_name):
		district_name = area_dict[area_name]
		csv_file = self.path_dict.get(district_name) + "/{0}_{1}.csv".format(district_name,area_name)
		print(csv_file)
		with open(csv_file,'w') as f:
			self.zufangs = self.get_area_zufang_info(city_name, area_name)
			if self.mutex.acquire(1):
				self.total_num += len(self.zufangs)
				self.mutex.release()
			for zufang in self.zufangs:
				f.write(zufang.text() + "\n")
		print("crawl area :{0} into {1}".format(area_name,csv_file))

	@staticmethod
	def get_area_zufang_info(city_name,area_name):
		total_page = 0
		zufang_list = list()
		district_name = area_dict[area_name]
		chinese_district = chinese_city_district_dict[district_name]
		chinese_area = chinese_area_dict[area_name]
		# print(chinese_district,chinese_area)
		url = "http://{0}.{1}.com/zufang/{2}".format(city_name, 'ke', area_name)
		# print(url)
		headers = create_headers()
		requests.adapters.DEFAULT_RETRIES = 5
		s = requests.session()
		s.keep_alive = False
		s.proxies = {"http": "111.231.10.150:1080", "http": "111.231.12.92:1080", "http": "111.231.7.214:1080"}
		response = s.get(url, timeout=10, headers=headers)
		html = response.content
		soup = BeautifulSoup(html,'lxml')
		# print(soup)

		#获得总页数
		try:
			page_box = soup.find_all('div',class_ = 'content__pg')
			match = re.search(r'.*data-totalpage="(\d+)".*',str(page_box))
			total_page = int(match.group(1))
			# print(match)
		except Exception as e:
			print(e)

		# 从第一页开始，遍历到最后一页
		for num in range(1,total_page + 1):
			headers = create_headers()
			url = "http://{0}.{1}.com/zufang/{2}/pg{3}".format(city_name, 'ke', area_name, num)
			requests.adapters.DEFAULT_RETRIES = 5
			s = requests.session()
			s.keep_alive = False
			s.proxies = {"http": "111.231.10.150:1080", "http": "111.231.12.92:1080", "http": "111.231.7.214:1080"}
			response = s.get(url, timeout=10, headers=headers)
			html = response.content
			soup = BeautifulSoup(html,'lxml')
			ul_element = soup.find('div',class_ = 'content__list')
			house_elements = ul_element.find_all('div',class_ = 'content__list--item')

			if len(house_elements) == 0:
				continue
			# else:
			# 	print(len(house_elements))

			for house_element in house_elements:
				price = house_element.find('span',class_ = 'content__list--item-price')
				desc1 = house_element.find('p',class_ = 'content__list--item--title')
				desc2 = house_element.find('p',class_ = 'content__list--item--des')

				try:
					price = price.text.replace(" ","").replace("元/月","")
					desc1 = desc1.text.strip().split(' ') # strip()去除首尾为空的字符
					desc2 = desc2.text.strip().replace(" ","").replace("\n","")
					xiaoqu = desc1[0]
					layout = desc1[1]
					size = desc2.split('/')[1].replace('㎡','平米')
					# print(size)
					#类实例化
					zufang = ZuFang(chinese_district, chinese_area, xiaoqu, layout, price, size)
					#存放zufang实例的list
					zufang_list.append(zufang)
				except Exception as e:
					print(e)

		return zufang_list

	def start(self):
		# 开始计时
		t1 = time.time()
		city = get_city()
		path_list = list()
		path_dict = dict()
		# print(city)
		#获取每个城市的区列表
		districts = get_districts(city)
		# print('City: {0}'.format(city))
		# print('Districts: {0}'.format(districts))

		#获取每个区的板块
		areas = list()
		for district in districts:
			area_of_district = get_areas(city,district)
			# print('{0} : Area_list : {1}'.format(district,area_of_district))
			areas.extend(area_of_district)
			#使用字典存储板块和区之间的映射关系
			for area in area_of_district:
				area_dict[area] = district
		# print('Area :',areas)
		# print('district and area :',area_dict)

		# 设置文件保存的路径，字典形式{'tianhe':'/data/zufang/gz/20190527/tianhe/',...}
		path_list = create_zufang_path(city,districts,self.date_string)
		self.path_dict = dict(zip(districts,path_list))
		print(path_dict)

		# self.collect_area_zufang_info('gz','shiqiao1')
		# 准备线程池用到的参数
		nones = [None for  i in range(len(areas)) ]
		city_list = [city for i in range(len(areas))]
		args = zip(zip(city_list,areas),nones)

        # 针对每个板块写一个文件,启动一个线程来操作
        # 如果传入的是个元组数据，那么他会把元组数据分开，做另外处理，元组中第一个元素为请求值 \
        # ，即给请求函数调用的值，第二个元素是结果值，就是请求函数执行后的输出值
		pool_size = thread_pool_size
		pool = threadpool.ThreadPool(pool_size)
		my_request = threadpool.makeRequests(self.collect_area_zufang_info, args)
		[pool.putRequest(req) for req in my_request]
		pool.wait()

		# 结束计时
		t2 = time.time()
		print("Total crawl {0} areas".format(len(areas)))
		print("Total cost {0} second to crawl {1} data items".format(t2 - t1,self.total_num))

if __name__ == '__main__':
	pass

