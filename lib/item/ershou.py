class ErShou(object):
    """docstring for ZuFang"""
    def __init__(self, district, area, xiaoqu, high, nianfen, layout, size, chaoxiang, \
                 danjia, zongjia, taxfree, house_link):
        self.district = district
        self.area = area
        self.xiaoqu = xiaoqu
        self.high = high
        self.nianfen = nianfen
        self.layout = layout
        self.size = size
        self.chaoxiang = chaoxiang
        self.danjia = danjia
        self.zongjia = zongjia
        self.taxfree = taxfree
        self.house_link = house_link
        # self.title = "地区，板块，小区，楼高，年份，布局，大小，朝向，单价，总价，其他，链接"

    def text(self):
        return self.district + "," + \
               self.area + "," + \
               self.xiaoqu + "," + \
               self.high + "," + \
               self.nianfen + "," + \
               self.layout + "," + \
               self.size + "," + \
               self.chaoxiang + "," + \
               self.danjia + "," + \
               self.zongjia + "," + \
               self.taxfree + "," + \
               self.house_link

    def text_json(self):
        result = dict()
        result = {"district": self.district, \
               "area": self.area, \
               "xiaoqu": self.xiaoqu, \
               "high": self.high,\
               "nianfen": self.nianfen, \
               "layout": self.layout, \
               "size": self.size, \
               "chaoxiang": self.chaoxiang, \
               "danjia": self.danjia, \
               "zongjia": self.zongjia, \
               "taxfree": self.taxfree, \
               "house_link": self.house_link}
        return result

    @staticmethod
    def title(self):
        return "地区" + "," + \
               "板块" + "," + \
               "小区" + "," + \
               "楼高" + "," + \
               "年份" + "," + \
               "布局" + "," + \
               "大小" + "," + \
               "朝向" + "," + \
               "单价" + "," + \
               "总价" + "," + \
               "税费" + "," + \
               "链接"

if __name__ == '__main__':
    re = ErShou(1,2,3,4,5,6,7,8,9,10,1)
    print(re.text_json())