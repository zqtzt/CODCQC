import numpy as np

def levels_order(qc_object,depth,tem,meta):
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

    kflagt1[np.where(depth_bak != depth_org)] = 1   
    return kflagt1,depth_bak,tem_bak