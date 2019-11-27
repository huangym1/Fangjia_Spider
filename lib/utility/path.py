import os
import sys
import inspect

def create_data_path():
	#获取当前文件所在的位置
    file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
    parent_path = os.path.dirname(file_path)
    lib_path = os.path.dirname(parent_path)
    root_path = os.path.dirname(lib_path)
    data_path = root_path + "/data" 
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return data_path

def create_zufang_path(city,districts,date):
    data_path = create_data_path()
    zufang_path_list = list()
    for district in districts:
        zufang_path = data_path + "/zufang" + "/" + date \
                      + "/" + city + "/" + district
        zufang_path_list.append(zufang_path)
        if not os.path.exists(zufang_path):
            os.makedirs(zufang_path)
    return zufang_path_list

def create_ershou_path(city,districts,date):
    data_path = create_data_path()
    ershou_path_list = list()
    for district in districts:
        ershou_path = data_path + "/ershou" + "/" + date \
                      + "/" + city + "/" + district
        ershou_path_list.append(ershou_path)
        if not os.path.exists(ershou_path):
            os.makedirs(ershou_path)
    return ershou_path_list

if __name__ == '__main__':
	create_zufang_path('gz','20190527')