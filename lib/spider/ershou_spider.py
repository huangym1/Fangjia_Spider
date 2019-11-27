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
from lib.item.ershou import *
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter


class ErShouBaseSpider(BaseSpider):
    def collect_area_ershou_info(self, city_name, area_name):
        self.district_name = area_dict[area_name]
        self.chinese_district_name = chinese_city_district_dict[self.district_name]
        self.chinese_area_name = chinese_area_dict[area_name]
        # print("start to [collect_area_ershou_info] for {0}-{1}\n".format(chinese_district_name, chinese_area_name))
        # 数据写入文档
        # district_name = area_dict[area_name]
        # csv_file = self.path_dict.get(district_name) + "/{0}_{1}.csv".format(district_name,area_name)
        # # print(csv_file)
        # with open(csv_file,'w') as f:
        #     self.ershous,self.nodata = self.get_area_ershou_info(city_name,area_name)
        #     if self.mutex.acquire(1):
        #         self.total_num += len(self.ershous)
        #         if len(self.nodata):
        #             self.nodata_list.append(self.nodata)
        #     self.mutex.release()
        #     f.write(self.title + "\n")
        #     for ershou in self.ershous:
        #         f.write(ershou.text() + "\n")
        # print("crawl area:{0} into {1}".format(area_name,csv_file))

        # 数据入库
        self.ershous, self.nodata = self.get_area_ershou_info(city_name, area_name)
        if self.mutex.acquire(1):
            self.num = len(self.ershous)
            self.total_num += self.num
            if len(self.nodata):
                self.nodata_list.append(self.nodata)
        self.mutex.release()
        for ershou in self.ershous:
            self.my_set.insert(ershou.text_json())
            # print(ershou.text_json())
        print("爬取:{0}-{1} 包含 {2} 条数据并入库. [目前共爬取:{3} 条数据]".format\
                  (self.chinese_district_name, self.chinese_area_name, self.num, self.total_num))

    @staticmethod
    def get_area_ershou_info(city_name, area_name):
        nodata = ""
        total_page = 0
        district_name = area_dict[area_name]
        chinese_district = chinese_city_district_dict[district_name]
        chinese_area = chinese_area_dict[area_name]
        ershou_list = list()
        url = "http://{0}.{1}.com/ershoufang/{2}".format(city_name, 'ke', area_name)
        headers = create_headers()
        responses = BaseSpider().proxy_request(url, headers)
        soup = BeautifulSoup(str(responses), 'lxml')

        # 获取总共页数
        try:
            page_box = soup.find('div', class_='page-box')
            match = re.search(r'.*totalPage":(\d+)', str(page_box))
            if (None == match):
                nodata = area_name
            else:
                total_page = int(match.group(1))
            # print(total_page)
        except Exception as e:
            print(e)

        # 从第一页遍历到最后
        for num in range(1, total_page + 1):
            headers = create_headers()
            url = "https://{0}.{1}.com/ershoufang/{2}/pg{3}/".format(city_name, 'ke', area_name, num)
            # 旧的方法
            # requests.adapters.DEFAULT_RETRIES = 5
            # proxy = BaseSpider().get_proxy()
            # s = requests.session()
            # s.keep_alive = False
            # s.proxies = {"http": "{}".format(proxy)}
            # response = s.get(url, timeout=10, headers=headers)

            # 调用基础类的方法
            responses = BaseSpider().proxy_request(url, headers)
            soup = BeautifulSoup(str(responses), 'lxml')

            house_elements = soup.find_all('div', class_='info clear')
            # print(house_element)

            if len(house_elements) == 0:
                continue

            for house_element in house_elements:
                house_info = house_element.find('div', class_='houseInfo'). \
                    text.strip().replace(' ', '').replace('\n', '').split('|')
                house_link = house_element.find('a')['href']
                if ("年" not in house_info[1]):
                    house_info_for_nianfen = house_info[0].split(")")
                    house_info_for_nianfen[0] = house_info_for_nianfen[0] + ")"
                    house_info.pop(0)
                    house_info.insert(0, house_info_for_nianfen[1])
                    house_info.insert(0, "暂无数据")
                    house_info.insert(0, house_info_for_nianfen[0])
                    # print(house_info)
                    # print(house_info_for_nianfen[0])
                xiaoqu = house_element.find('div', class_='positionInfo').text.replace('\n', '')
                high = house_info[0]
                nianfen = house_info[1]
                layout = house_info[2]
                size = house_info[3]
                chaoxiang = house_info[-1]
                price = house_element.find('div', class_='unitPrice').text.replace('单价', '').replace('\n', '')
                totalprice = house_element.find('div', class_='totalPrice').text
                taxfree = house_element.find('div', class_='tag').find('span',
                                                                       attrs={"class": re.compile(r'two|taxfree')})
                if (None == taxfree):
                    taxfree = "暂无数据"
                else:
                    taxfree = taxfree.text
                # print(xiaoqu, high, nianfen, layout, size, chaoxiang, price, totalprice, taxfree)

                try:
                    ershou = ErShou(chinese_district, chinese_area, xiaoqu, high, \
                                    nianfen, layout, size, chaoxiang, price, totalprice, taxfree, house_link)
                    ershou_list.append(ershou)
                except Exception as e:
                    print(e)

        return ershou_list, nodata

    def recollect_area_ershou_info(self,city, areas):
        num = 1
        print("现在开始第{}次复爬数据".format(num))
        for area in areas:
            self.collect_area_ershou_info(city, area)

        return

    def start(self):
        path_dict = dict()
        nodata = list()
        # 开始计时
        t1 = time.time()
        city = get_city()  # 通过终端获取输入的城市
        districts = get_districts(city)  # 获取每个城市的区列表
        # 获取每个区的板块
        areas = list()
        for district in districts:
            area_of_district = get_areas(city, district)
            # 使用字典存储板块和区之间的映射关系
            if area_of_district != None:
                areas.extend(area_of_district)
                for area in area_of_district:
                    if area != None:
                        area_dict[area] = district
                    else:
                        print("area:{}".format(area))
            else:
                print("area_of_district:{}".format(area_of_district) )


        # print('Area :',areas)
        # print('district and area :',area_dict)

        # 设置文件保存的路径，字典形式{'tianhe':'/data/zufang/gz/20190527/tianhe/',...}
        path_list = create_ershou_path(city, districts, self.date_string)
        self.path_dict = dict(zip(districts, path_list))
        # print(path_dict)

        # 准备线程用到的参数，构造(（city_name,area_name),result)这样的元组列表
        result = (None for i in range(len(areas)))
        city_list = (city for i in range(len(areas)))
        args = zip(zip(city_list, areas), result)

        # 针对每个板块写一个文件,启动一个线程来操作
        # 如果传入的是个元组数据，那么他会把元组数据分开，做另外处理，元组中第一个元素为请求值 \
        # ，即给请求函数调用的值，第二个元素是结果值，就是请求函数执行后的输出值
        # print("延迟5秒...")
        # time.sleep(5)
        pool_size = thread_pool_size
        pool = threadpool.ThreadPool(pool_size)
        my_request = threadpool.makeRequests(self.collect_area_ershou_info, args)
        [pool.putRequest(req) for req in my_request]
        pool.wait()

        # 结束计时
        t2 = time.time()
        print("总共爬取 {0} 个areas".format(len(areas)))
        print("总共耗时 {0} 秒爬取 {1} 条数据".format(t2 - t1, self.total_num))
        for i in self.nodata_list:
            self.chinese_nodata_list.append(chinese_area_dict[self.nodata_list[i]])
        if self.nodata_list != None:
            print("以下板块没有获取到数据:... \n {0}".format(self.chinese_nodata_list))
            self.recollect_area_ershou_info(city, self.nodata_list)
        else:
            print("所有数据已爬取完成，数据完整..")

        return

if __name__ == '__main__':
    ershou = ErShouBaseSpider()
    # ershou.start()
    # ershou.collect_area_ershou_info('gz','meihuayuan')
