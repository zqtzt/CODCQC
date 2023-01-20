import numpy as np
from CODCQC.util import CODCQC_constant as const
import numpy.ma as ma

def number_of_temperature_extrema(qc_object,depth, tem, meta):
    levels = meta.levels
    kflagt = np.zeros(levels, int)
    if (levels < const.levminext): #  '<levminext,no temp_extrema check'
        return kflagt

    try:
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    except:
        depth = ma.array(depth, mask=np.isnan(depth))
        tem = ma.array(tem, mask=np.isnan(tem))
        isData = np.logical_and(depth.mask == False, tem.mask == False)

    tem_diff = np.diff(tem)
    pa = np.abs(tem_diff[:-1])
    pb = np.abs(tem_diff[1:])
    pmin = np.min(np.vstack((pa, pb)).transpose(), axis=1)
    np.where(tem_diff[:-1] * tem_diff[1:] < 0)
    index = np.logical_and(tem_diff[:-1] * tem_diff[1:] < 0, pmin > const.deltaext)  # 等价于找牛眼且牛眼要大于delataext
    index = np.insert(index, 0, False)
    index = np.insert(index, -1, False)

    kflagt[index] = 1  # spike location 
    if (np.sum(kflagt == 1) > const.maxextre):  # number of spikes > 4, flag the whole profile
        kflagt[:] = 1
        
    kflagt[depth<10]=0
    
    return kflagt