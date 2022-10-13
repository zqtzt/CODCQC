import numpy as np
import numpy.ma as ma

def spike_check(qc_object,depth, tem, meta):
    try:
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    except:
        depth = ma.array(depth, mask=np.isnan(depth))
        tem = ma.array(tem, mask=np.isnan(tem))
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    levels = meta.levels
    kflagt = np.zeros(levels, np.int)
    if (levels < 3):
        return kflagt

    spike = np.full(levels, np.nan)
    for i in range(1, levels - 1):
        if (~isData[i]):
            continue
        depth13 = depth[i + 1] - depth[i - 1]
        depth12 = depth[i] - depth[i - 1]
        depth23 = depth[i + 1] - depth[i]
        dzmax = 50.0 + depth[i] / 10.0
        dzmax2 = dzmax / 2
        if (depth13 > dzmax or depth12 > dzmax2 or depth23 > dzmax2):
            continue
        v1 = tem[i - 1]
        v2 = tem[i]
        v3 = tem[i + 1]
        a = 0.5 * (v3 + v1)
        q1 = abs(v2 - a)
        q2 = abs(0.5 * (v3 - v1))
        spike[i] = q1 - q2

    # Set spike overall limits depends on depth interval: thershold (depth dependent thershold values)
    spikemax = 4.0
    index1 = np.logical_and(spike > spikemax, depth <= 1000)
    kflagt[index1] = 1
    spikemax = 3.0
    index1 = np.logical_and(np.logical_and(spike > spikemax, depth > 1000), depth < 2000)
    kflagt[index1] = 1
    spikemax = 2.0
    index1 = np.logical_and(spike > spikemax, depth >= 2000)
    kflagt[index1] = 1
    return kflagt