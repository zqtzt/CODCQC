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
    # NO CHECK FOR CASPIAN  
    if (rlat >= 35 and rlat <= 45 and rlon >= 45 and rlon <= 60):
        return kflagt
    elif (rlat >= 40 and rlat <= 50 and rlon >= -95 and rlon <= -75):  # NO CHECK FOR GREAT LAKES
        descrption = 'NO CHECK FOR GREAT LAKES'
        return kflagt


    if (np.isnan(gebcodepth)):
        return kflagt  # no check possible

    if (gebcodepth <= -5):  # observed on the land
        kflagt[:] = 1
        return kflagt
        


    kflagt[np.where(depth >= gebcodepth)] = 1  # 大于此容错深度之下的，全部标记为1
    return kflagt
