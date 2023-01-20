import numpy as np


def constant_value(qc_object,depth, tem, meta):
    isData = np.logical_and(depth.mask == False, tem.mask == False)
    typ3 = meta.typ3
    levels = meta.levels
    kflagt = np.zeros(levels, int)
    if(levels<=2):
        return kflagt

    # criteria for the minimum number of levels within the thermostad
    minlevstad = 7  #  the number of such exactly the same temperature value within the layer.
    if (typ3 == 'OSD'):
        minlevstad = 10
    elif (typ3 == 'APB' or typ3 == 'XBT' or typ3 == 'PFL' or typ3 == 'PF' or typ3 == 'XB'):
        minlevstad = 20
    elif (typ3 == 'CTD' or typ3 == 'CD' or typ3 == 'CT' or typ3 == 'CU' or typ3 == 'MC' or typ3 == 'XC'):
        minlevstad = 50

    # minimum thickness of the thermostad layer
    thickmin = 300.0  # subjective
    if (meta.lat >= 65 or meta.lat <= -65):  # Polar region 
        thickmin = 400.0
    if (levels <= minlevstad):  # no check for short profiles
        return kflagt
    num = np.full(levels, np.nan)
    for k in range(levels - minlevstad):
        num[k] = np.nansum(np.abs(tem[k:] - tem[k]) <= 0.001) 
    num[np.logical_or(tem < -2, ~isData)] = np.nan
    num = num[~np.isnan(num)]
    try:
        numa = np.nanmax(num)
        kuma = np.argmax(num)
    except:
        numa = 0
        kuma = 0

    if (numa >= minlevstad):
        z1 = depth[kuma]
        z2 = depth[int(kuma + numa - 1)]
        thick = z2 - z1
        # 判断观测到恒温层的厚度是否比我“理论上”的厚度要大，如果大的话，那么，这个区间的所有测量值，都被认为是异常值
        if (thick >= thickmin):
            kflagt[int(kuma):int(kuma + numa)] = 1  # flag levels within the stad
            if ('XBT' in typ3 or 'xb' in typ3 or 'xbt' in typ3):
                kflagt[int(kuma):] = 1  

    return kflagt