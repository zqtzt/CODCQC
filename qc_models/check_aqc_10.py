## Multiple extrema check
'''
This check identifiers profiles with unrealistically big number of local temperature extrema, 
The thresholds has considered the measurement precision or the typical size of the micro-scale tempearature inversions. 
Values exceed the temperature extrema are flagged as 1.
'''
from COMSQC.util import aqc_constant as const
import numpy as np
import numpy.ma as ma

def number_of_temperature_extrema(depth,tem,meta):

    levels = meta.levels
    kflagt = np.zeros(levels, int)
    if(levels < const.levminext):
        #descrption = '<levminext,no temp_extrema check'
        return kflagt

    try:
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    except:
        depth=ma.array(depth,mask=np.isnan(depth))
        tem = ma.array(tem, mask=np.isnan(tem))
        isData = np.logical_and(depth.mask == False, tem.mask == False)

    tem_diff=np.diff(tem)
    pa=np.abs(tem_diff[:-1])
    pb=np.abs(tem_diff[1:])
    pmin=np.min(np.vstack((pa,pb)).transpose(),axis=1)
    np.where(tem_diff[:-1]*tem_diff[1:] <0 )
    index=np.logical_and(tem_diff[:-1] * tem_diff[1:] < 0, pmin > const.deltaext)  #find the extreme values (greater than a thresholds --delataext)
    index=np.insert(index,0,False)
    index = np.insert(index, -1, False)

    kflagt[index]=1  #flagged 
    if(np.sum(kflagt==1)>const.maxextre):  #If number of extereme value is greater than 4, all observations in the profile are flagged
        kflagt[:]=1

    return kflagt






