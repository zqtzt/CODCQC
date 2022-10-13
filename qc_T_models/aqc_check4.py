import numpy as np

def gebo_check(qc_object,depth, tem, meta):
    rlat = meta.lat
    rlon = meta.lon
    levels = meta.levels
    kflagt = np.zeros(levels, np.int)
    typ3 = meta.typ3
    gebcodepth = meta.gebcodepth


    if ('MRB' in typ3 or 'moored buoy' in typ3):
        return kflagt
    if (rlon > 360):
        return kflagt
    # NO CHECK FOR CASPIAN  这些区域要画出来
    if (rlat >= 35 and rlat <= 45 and rlon >= 45 and rlon <= 60):
        return kflagt
    elif (rlat >= 40 and rlat <= 50 and rlon >= -95 and rlon <= -75):  # NO CHECK FOR GREAT LAKES
        descrption = 'NO CHECK FOR GREAT LAKES'
        return kflagt

    # # #计算gebco
    # try:
    #     jy = np.where(np.logical_and(rlat > qc_object.gebco_lat_bnd[:, 0], rlat <= qc_object.gebco_lat_bnd[:, 1]))[0][
    #         0]  # 纬度
    #     ix = np.where(np.logical_and(rlon > qc_object.gebco_lon_bnd[:, 0], rlon <= qc_object.gebco_lon_bnd[:, 1]))[0][
    #         0]  # 经度
    # except:
    #     return kflagt
    # if ((ix < 0 or ix > 86400) or (jy < 0 or jy > 43200)):
    #     # descrption = 'no find ix,jy,no climatology check'
    #     return kflagt
    #
    # gebcodepth = qc_object.elevation[ix][jy]
    # gebcodepth = -(gebcodepth)  # 把深度弄成正，数值为正代表海洋，为负代表陆地
    #
    # if (gebcodepth <= -9998.0):
    #     return kflagt  # no check possible

    if (np.isnan(gebcodepth)):
        return kflagt  # no check possible

    if (gebcodepth <= -5):  # 观测位置在陆地上，全部深度都拒绝，标记为1
        kflagt[:] = 1
        return kflagt
        
    # # GEBCP-DEPTH with tolerance   !这个常数10.0 和0.05可以自己调整
    # if (meta.lat > -60):
    #     if gebcodepth < 15:
    #         dtol = gebcodepth + 35.0 + gebcodepth * 0.087
    #     elif (gebcodepth < 1000):
    #         dtol = gebcodepth + 30 + gebcodepth * 0.087
    #     else:
    #         dtol = gebcodepth + 80
    # else:
    #     if (gebcodepth < 600):
    #         dtol = gebcodepth + 270 - gebcodepth * 0.037
    #     else:
    #         dtol = gebcodepth + 80

    kflagt[np.where(depth >= gebcodepth)] = 1  # 大于此容错深度之下的，全部标记为1
    return kflagt
