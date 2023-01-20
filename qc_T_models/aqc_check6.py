import numpy as np
import gsw

def freezing_point_check(qc_object,depth,tem,meta):
    levels = meta.levels
    if(meta.lat<65 and meta.lat>-65):  ####no check for polar regions
        kflagt = np.zeros(levels, np.int)
        return kflagt
    try:
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    except:
        depth=ma.array(depth,mask=np.isnan(depth))
        tem = ma.array(tem, mask=np.isnan(tem))
        isData = np.logical_and(depth.mask == False, tem.mask == False)
        
    rlat=meta.lat
    rlon=meta.lon
    kflagt=np.zeros(levels,np.int)
    try:
        jy=np.where(np.logical_and(rlat>qc_object.lat_bound[0,:] , rlat <= qc_object.lat_bound[1,:]))[0][0]  #纬度
        ix = np.where(np.logical_and(rlon > qc_object.lon_bound[0, :], rlon <= qc_object.lon_bound[1, :]))[0][0]  #经度
    except:
        return kflagt
    if((ix < 0 or ix > 361) or (jy <0 or jy > 181)):
        descrption = 'no find ix,jy,no climatology check'
        return kflagt

    # find depth-index for MIN/MAX-fields from depth values
    depth_index=[]
    for k in range(levels):
        if(~isData[k]):
            depth_index.append(1)
            continue
        try:
            depth_index.append(np.where(np.logical_and(depth[k] >= qc_object.Std_depth_41_bound[0, :], depth[k] < qc_object.Std_depth_41_bound[1, :]))[0][0])
        except:
            depth_index.append(40)

    salinity_clim = np.squeeze(qc_object.Savg[ix, jy, depth_index, meta.month-1])
    salinity_clim[np.isnan(salinity_clim)] = 34.7
    pressure = gsw.p_from_z(-depth, rlat)

    T_freezing=cal_freezing_point(pressure,salinity_clim)
    kflagt[tem < T_freezing] = 1
    return kflagt


def cal_freezing_point(pressure,salinity):
    #pressure: dbar
    #salinity: psu([27, 35])
    salinity[np.logical_or(salinity < 27,salinity > 35)] = np.nan
    T_freezing = -0.0575 * salinity + (1.710523e-3) * np.power(salinity, 3.0 / 2) - (2.154996e-4) * salinity * salinity - (7.53e-4) * pressure

    return T_freezing