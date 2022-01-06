#Global crude range check
'''
This test identifiers whether the observation are in gross error. 
The tempearture depth-dependent (upper and lower) threshold (mask) is defined by 99% quantile based on global statisitcal result. 
Values exceed the overall depth-dependent range are flagged as 1.
Note that in some specific regions at some depth (e.g., above 4000m in the Mediterranean Sea) , the observation is not tested in this check.
'''
import numpy as np
import numpy.ma as ma
from COMSQC.util import aqc_constant as const
def crude_range(depth,tem,meta):
    levels=meta.levels
    rlat=meta.lat
    rlon=meta.lon
    try:
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    except:
        depth=ma.array(depth,mask=np.isnan(depth))
        tem = ma.array(tem, mask=np.isnan(tem))
        isData = np.logical_and(depth.mask == False, tem.mask == False)

    kflagt2=np.zeros(levels,int)

    kflagt2[np.where(tem < const.parminover) or np.where(tem > const.parmaxover)]=1

    
    for i in range(levels):
        if(~isData[i]):
            kflagt2[i] = 1
            continue
        #go for crude check
        index=np.where(np.logical_and(depth[i] >= const.depth_left, depth[i] < const.depth_right))
        if(np.logical_or(tem[i]<const.tzlim1_zhetao[index], tem[i]>const.tzlim2_zhetao[index])):
            kflagt2[i]=1

    ##no check for some special regions at some depths
    if((rlat >=30 and rlat <=47) or (rlon >= -6 and rlon <=54)):  #MED
        kflagt2[np.where(depth<=4000)]=0
    elif ((rlat >=10 and rlat <=30) or (rlon >= 30 and rlon <=45)): #Red Sea
        kflagt2[np.where(depth <= 2000)]=0
    elif((rlat >=17 and rlat <=30) or (rlon >= -100 and rlon <=-82) ): # Gulf of Mexico
        kflagt2[np.where(depth > 2000)] = 0
    elif((rlat >=8 and rlat <=18) or (rlon >= -82 and rlon <=-65)): # Gulf of Mexico
        kflagt2[np.where(depth > 2000)] = 0
    elif ((rlat >= 18 and rlat <= 22) or (rlon >= -82 and rlon <= -75)):
        kflagt2[np.where(depth > 2000)] = 0
    elif ((rlat >= 18 and rlat <= 20) or (rlon >= -77 and rlon <= -72)):
        kflagt2[np.where(depth > 2000)] = 0

    return kflagt2
