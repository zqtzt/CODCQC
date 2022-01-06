## Local maximum depth check
'''
This check identifiers whether the deepest sampled level is larger than the bottom depth according to the digital global bathymetry GEBCO2.  
Values exceed the bottom depth are flagged as 1.
'''
import numpy as np
import numpy.ma as ma
from COMSQC.util import aqc_constant as const
def gebo_check(depth,tem,meta):
    rlat=meta.lat
    rlon=meta.lon
    levels=meta.levels

    kflagt3=np.zeros(levels,np.int)

    if(rlon > 180 and rlon <=360):
        meta.lon=meta.lon-360
    elif (rlon >360):
        return kflagt3

    #NO CHECK FOR CASPIAN  
    if(rlat >=35 and rlat <= 45 and rlon >=45 and rlon<=60):
        return kflagt3
    elif (rlat >= 40 and rlat <= 50 and rlon >= -95 and rlon <= -75):  
        #NO CHECK FOR GREAT LAKES
        return kflagt3

    ##read the local bottom depth according to the GEBCO depth file
    try:
        jy = np.where(np.logical_and(rlat > const.gebco_lat_bnd[:, 0], rlat <= const.gebco_lat_bnd[:, 1]))[0][0]  # 纬度
        ix = np.where(np.logical_and(rlon > const.gebco_lon_bnd[:, 0], rlon <= const.gebco_lon_bnd[:, 1]))[0][0]  # 经度
    except:
        return kflagt3
    if((ix < 0 or ix > 86400) or (jy <0 or jy > 43200)):
        # descrption = 'no find ix,jy,no climatology check'
        return kflagt3

    gebcodepth=const.elevation[ix][jy]
    gebcodepth=-(gebcodepth)   #ocean depth are postiive, land are negative

    if(gebcodepth <= -9998.0):
        return kflagt3  #no check possible

    if(gebcodepth <= -5):  #position on land (has a tolerant value) 
        kflagt3[:]=1
        return kflagt3


    #GEBCO-DEPTH with tolerance  
    if gebcodepth<10: #coastline
        dtol = gebcodepth + 20.0 + gebcodepth * 0.05
    else:
        dtol=gebcodepth+15.0 +gebcodepth*0.05

    kflagt3[np.where(depth >= dtol)]=1  


    return kflagt3




