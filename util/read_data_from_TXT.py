# -*- coding：utf-8 -*-
# read input data from *.txt file
def data_reading(txt_file):
    flag = 0
    meta_list = []
    depth_all = []
    tem_all = []
    for line in open(txt_file, "r"):
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        if 'HH' in line:
            if (flag == 1):
                depth_all.append(depth)
                tem_all.append(tem)
                flag = 0
            if (flag == 0):
                depth = []
                tem = []
                handle = line.split(' ')
                while '' in handle:
                    handle.remove('')
                meta_list.append(handle)
                flag = 1
        else:
            data = line.strip('\n').split(' ')
            while '' in data:
                data.remove('')
            depth_sample, tem_sample = [float(x) for x in data[:2]]
            depth.append(depth_sample)
            tem.append(tem_sample)

    depth_all.append(depth)
    tem_all.append(tem)

    return depth_all,tem_all,meta_list