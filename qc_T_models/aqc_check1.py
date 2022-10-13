import numpy as np

def basic_information_check(qc_object,depth,tem,meta):
    kflagt = np.zeros(meta.levels, np.int)
    discard_flag = 0
    if (meta.year <= 1750 or meta.year > 2022 or np.isnan(meta.year)):
        kflagt = np.full(meta.levels, 1)  # 这里后面要改成1
        discard_flag = 1
        
    if (meta.month < 1 or meta.month > 12 or np.isnan(meta.month)):
        meta.month = 6  # 这些地方都可以在未来改进，用一个新label标记信息缺失
        
    if (meta.lat < -83 or meta.lat > 90 or np.isnan(meta.lat)):
        kflagt = np.full(meta.levels, 1)
        discard_flag = 1
        
    if (meta.lon > 180 and meta.lon <= 360):
        meta.lon = meta.lon - 360.0  #####经纬度全部转换成正负180范围内
        
    if (meta.lon < -180.1 or meta.lon > 180):
        kflagt = np.full(meta.levels, 1)
        discard_flag = 1
        
    if (np.isnan(meta.lat) or np.isnan(meta.lon)):
        kflagt = np.full(meta.levels, 1)
        discard_flag = 1
        
    if (len(depth) == 0 or len(tem) == 0):
        kflagt = np.full(meta.levels, 1)
        discard_flag = 1
        
    if (len(depth) != len(tem)):  # 深度和温度不对应，异常剖面
        levels = np.max((len(depth), len(tem)))
        kflagt = np.full(levels, 0)  ###先改成0，后面再改回去
        discard_flag = 1

    return kflagt, discard_flag,meta