## check stuck value  Constant value check
'''
This check temperature profile for stuck value or unrealistically thick thermostad. It is refered (Gourestki, 2018). 
All measurements detected as stuck value or whin the unrealisitical thick thremostad are flagged as 1.
'''
import numpy as np

def constant_value(depth,tem,meta):
    isData = np.logical_and(depth.mask == False, tem.mask == False)
    typ3=meta.typ3
    levels=meta.levels

    kflagt5=np.zeros(levels,int)


    #criteria for the minimum number of levels within the thermostad
    minlevstad=7  #the number of such exactly the same temperature value within the layer.
    if(typ3=='OSD'):
        minlevstad=10
    elif(typ3=='APB' or typ3=='XBT' or typ3=='PFL' or typ3== 'PF' or typ3=='XB'):
        minlevstad=20
    elif(typ3=='CTD' or typ3== 'CD' or typ3=='CT' or typ3=='CU' or typ3=='MC' or typ3=='XC'):
        minlevstad=50

    #minimum thickness of the thermostad layer  
    thickmin=300.0  #subjective value
    if(meta.lat>=65 or meta.lat<=-65): #Polar region increases to 400 meters
        thickmin = 400.0

    if(levels <= minlevstad):  #no check for short profiles
        return kflagt5

    num=np.full(levels,np.nan)
    for k in range(levels-minlevstad):
        num[k]=np.nansum(np.abs(tem[k:]-tem[k])<=0.001)   #identified as constant value
    num[np.logical_or(tem<-2,~isData)]=np.nan

    # 去掉nan值
    num = num[~np.isnan(num)]
    try:
        numa=np.nanmax(num)
        kuma=np.argmax(num)
    except:
        numa=0
        kuma=0
    # print(numa)
    # print(kuma)

    if(numa >= minlevstad):
        z1=depth[kuma]
        z2=depth[int(kuma+numa-1)]
        thick=z2-z1
        # whether exceeds the minimum thickness of the thermostad layer  
        if(thick >=thickmin):
            kflagt5[int(kuma):int(kuma+numa)]=1  #flag levels within the stad
            if('XBT' in typ3 or 'xb' in typ3 or 'xbt' in typ3):
                kflagt5[int(kuma):]=1   #Flags all data in XBT profiles

    return kflagt5

if __name__ == '__main__':
    import numpy as np
    typ3='MBT'
    depth=np.array([1,5,30,60,100,150,200,400,600,800,850,900,920],np.float)
    tem=np.array([24,23,22,18.0,18.0,18.0,18.0,18.0,18.0,18.0,18.0,18.0,np.nan],np.float)
    # depth = np.array([1, 5, 10, 20, 25, 30, 40, 50, 60, 80, 100], np.float)
    # tem = np.array([24, 23, 22, 21.0, 20.5, 20.0, 19.0, 18.0, 17.0, 17.0, 16.0], np.float)

    class metaData(object):
        def __init__(self):
            pass

    meta=metaData()
    meta.typ3=typ3
    meta.levels=len(tem)
    meta.lat=33
    meta.lon=140
    kflagt5=constant_value(depth,tem,meta)
    print(kflagt5)


