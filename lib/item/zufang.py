
class ZuFang(object):
	"""docstring for ZuFang"""
	def __init__(self, district, area, xiaoqu, layout, jiage, size):
		self.district = district
		self.area = area
		self.xiaoqu = xiaoqu
		self.layout = layout
		self.jiage = jiage
		self.size = size

	def text(self):
		return self.district + "," + \
				self.area + "," + \
				self.xiaoqu + "," + \
				self.layout + "," + \
				self.jiage + "," + \
				self.size
		