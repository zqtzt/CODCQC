'''
This test identifiers whether the sample depth levels are placed in increasing order. 
If an depth measurement is not an increasing depth value, this observations are flagged as 1.
'''
import numpy as np
import numpy.ma as ma
from COMSQC.util import aqc_constant as const
def levels_order(depth,tem,meta):
    # tem=np.array(tem)
    # depth=np.array(depth)
    #取有效值
    depth_bak=depth
    depth_org = np.copy(depth)
    tem_bak=tem
    try:
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    except:
        depth=ma.array(depth,mask=np.isnan(depth))
        tem = ma.array(tem, mask=np.isnan(tem))
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    depth=depth[isData]
    tem=tem[isData]

    # levels=meta.levels
    kflagt1=np.zeros(meta.levels,np.int)

    #sort
    order=np.argsort(depth)
    depth=depth[order]
    tem=tem[order]

    depth_bak[isData]=depth.data
    tem_bak[isData]=tem.data

    kflagt1[np.where(depth_bak != depth_org)] = 1   #我觉得把它订正调换好熟顺序之后就行了，不需要标记吧，这个可以在以后多分类的时候标记been modified

    return kflagt1,depth_bak,tem_bak


if __name__ == '__main__':
    import numpy as np
    depth=np.array([1,-1,2,3,5,4,7,8,9,11,10])
    tem=np.array([25,26,24.5,24,23,22,21,20,19,18,17])
    [depth,tem,kflagt1]=levels_order(depth,tem,len(depth))
