## basic information check (date,time,location)
'''
This test identifies the date/time/location of the selceted profile based on the general information.
For example, the year should be falled inside the range [1750, 2022], 
the latitude should be falled inside the range [-83, 90] etc. 
All observations in the slected profile are flagged as 1 when the metadata falls outside the general information range. 
'''
import numpy as np
from COMSQC.util import aqc_constant as const

def basic_information_check(depth,tem,meta):

    kflagt=np.zeros(meta.levels,np.int)
    discard_flag=0

    if (meta.year <= 1750 or meta.year > 2022 or np.isnan(meta.year) or abs(meta.year-const.dummy_value)<0.001):
        kflagt = np.full(meta.levels, 1)  # 这里后面要改成1
        discard_flag = 1
    if (meta.month < 1 or meta.month > 12 or np.isnan(meta.month) or abs(meta.month-const.dummy_value)<0.001):
        meta.month = 6  # 这些地方都可以在未来改进，用一个新label标记信息缺失
    if (meta.lat < -83 or meta.lat > 90 or np.isnan(meta.lat) or abs(meta.lat-const.dummy_value)<0.001):
        kflagt = np.full(meta.levels, 1)
        discard_flag = 1
    if (meta.lon > 180 and meta.lon <= 360):
        meta.lon = meta.lon - 360.0  #####经纬度全部转换成正负180范围内
    if (meta.lon < -180 or meta.lon > 180):
        kflagt = np.full(meta.levels, 1)
        discard_flag = 1

    if (np.isnan(meta.lat) or np.isnan(meta.lon)):
        kflagt = np.full(meta.levels, 1)
        discard_flag = 1

    if(len(depth)==0 or len(tem)==0):
        kflagt = np.full(meta.levels, 1)
        discard_flag=1

    if (len(depth) != len(tem)):  # 深度和温度不对应，异常剖面
        levels = np.max((len(depth), len(tem)))
        kflagt = np.full(levels, 0)  ###先改成0，后面再改回去
        discard_flag = 1

    #小于0的标记成1，并且mask_array设置成NaN
    if(not discard_flag):
        kflagt[depth<0]=1

    return kflagt
