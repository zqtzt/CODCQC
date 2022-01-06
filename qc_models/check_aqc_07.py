#Local climatology check
'''
This check aims at determining whether the observed values fall within an acceptable local climatological temonrature range in a local scale. 
The IAP-T-range is used as the local climatological temperature range.
Value that falls outside the local monthly depth-dependent range are flagged as 1.
'''
import numpy as np
import numpy.ma as ma
from COMSQC.util import aqc_constant as const
def climatology_check(depth,tem,meta):
    try:
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    except:
        depth=ma.array(depth,mask=np.isnan(depth))
        tem = ma.array(tem, mask=np.isnan(tem))
        isData = np.logical_and(depth.mask == False, tem.mask == False)
    levels=meta.levels
    rlat=meta.lat
    rlon=meta.lon
    month=meta.month

    tmin_array=[]
    tmax_array=[]

    kflagt=np.zeros(levels,np.int)
    if(levels==0):
        return kflagt,tmin_array,tmax_array

    # find grid-index for MIN/MAX-fields from lat/lon values
    if (rlon > 180 and rlon<=360):
        rlon=rlon-360
    try:
        jy=np.where(np.logical_and(rlat>const.lat_bound[0,:] , rlat <= const.lat_bound[1,:]))[0][0]  #纬度
        ix = np.where(np.logical_and(rlon > const.lon_bound[0, :], rlon <= const.lon_bound[1, :]))[0][0]  #经度
    except:
        return kflagt, tmin_array, tmax_array

    if((ix < 0 or ix > 361) or (jy <0 or jy > 181)):
        descrption = 'no find ix,jy,no climatology check'
        # print(descrption)
        return kflagt,tmin_array,tmax_array

    # find depth-index for MIN/MAX-fields from depth values
    depth_index=[]
    for k in range(levels):
        if(~isData[k]):
            depth_index.append(np.nan)
            continue
        try:
            depth_index.append(np.where(np.logical_and(depth[k] >= const.Std_depth_bound[0, :], depth[k] < const.Std_depth_bound[1, :]))[0][0])
        except:
            depth_index.append(np.nan)

    #find local upper and lower temperature bounds according to the IAP-T-range climatology
    for i in range(levels):
        if(np.isnan(depth_index[i])):
            tmin_array.append(const.parminover)
            tmax_array.append(const.parmaxover)
            continue

        if (depth_index[i] < 79):  #monthly bases above 2000m
            tmina=const.tmin[ix,jy,depth_index[i],month-1]
            tmaxa=const.tmax[ix,jy,depth_index[i],month-1]
            if (tmina <= const.parminover or np.isnan(tmina)):
                tmina = const.parminover
            if(tmaxa >= const.parmaxover  or np.isnan(tmaxa)):
                tmaxa = const.parmaxover

        elif (depth_index[i]>=79 and depth_index[i] <= 98):  #seasonal bases at 2000-4000m
            if month in [3, 4, 5]:
                imonth=14  #spring
            elif month in [6, 7, 8]:
                imonth=15  #summer
            elif month in [9, 10, 11]:
                imonth=16  #autumn
            elif month in [12, 1, 2]:
                imonth=13  #winter
            tmina=const.tmin[ix,jy,depth_index[i]-79,imonth-1]
            tmaxa=const.tmax[ix,jy,depth_index[i]-79,imonth-1]
            if (tmina <= const.parminover or np.isnan(tmina)):
                tmina = const.parminover
            if(tmaxa >= const.parmaxover  or np.isnan(tmaxa)):
                tmaxa = const.parmaxover
        elif (depth_index[i]>98): #'All year' climatology bases below 4000m
            tmina=const.tmin[ix,jy,depth_index[i]-99,16]
            tmaxa=const.tmax[ix,jy,depth_index[i]-99,16]
            if (tmina <= const.parminover or np.isnan(tmina)):
                tmina = const.parminover
            if(tmaxa >= const.parmaxover  or np.isnan(tmaxa)):  
                tmaxa = const.parmaxover

        tmin_array.append(tmina)
        tmax_array.append(tmaxa)


    # input torlerance for the bound and start flagging
    type_advanced=['CTD','CT','CU','ctd','PFL','pfl','profiling','DRB','Drifting']
    if(meta.typ3 in type_advanced):
        tmin_array=np.array(tmin_array)
        tmin_array=tmin_array-np.abs(tmin_array)*0.04
        tmax_array=np.array(tmax_array)
        tmax_array=tmax_array+np.abs(tmax_array)*0.04
        kflagt[np.logical_or(tem < tmin_array, tem > tmax_array)] = 1
    else:
        tmin_array=np.array(tmin_array)
        tmin_array=tmin_array-np.abs(tmin_array)*0.01
        tmax_array=np.array(tmax_array)
        tmax_array=tmax_array+np.abs(tmax_array)*0.01
        kflagt[np.logical_or(tem < tmin_array, tem > tmax_array)] = 1


    if('DRB' in meta.typ3 or 'Drifting' in meta.typ3): #no checks for DRB greater than 760m
        kflagt[depth>760]=0


    return kflagt,tmin_array,tmax_array


if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'F:\\QC_science\\QC_viktor\\My_AQC\\')
    import numpy as np
    import aqc_constant as const

    # print('Starting reading climatology file...')
    # data = np.load('../climatology_tmin_tmax.npz')
    # tmin = data['tmin']
    # tmax = data['tmax']

    # from f2py_function import getwaghclevels as GetStandLev
    # [maxim,zedqc]= GetStandLev.getwaghclevels()

    rlat=-12.4667
    rlon=129.033
    # depth=[1,3,5,10,15,30,40,50,700,800]
    depth=[3.77981996536255, 4.40963983535767, 5.03942012786865, 5.66914987564087, 6.29884004592896, 6.92849016189575, 7.55809020996094, 8.18764972686768, 8.81717014312744, 9.44664001464844, 10.0760698318481, 10.7054595947266, 11.3347997665405, 11.9640998840332, 12.5933599472046, 13.2225704193115, 13.8517503738403, 14.4808702468872, 15.1099596023560, 15.7390003204346, 16.3680000305176, 16.9969501495361, 17.6258697509766, 18.2547302246094, 18.8835601806641, 19.5123405456543, 20.1410808563232, 20.7697792053223, 21.3984298706055, 22.0270404815674, 22.6556091308594, 23.2841300964355, 23.9126091003418, 24.5410499572754, 25.1694393157959, 25.7977905273438, 26.4260997772217, 27.0543594360352, 27.6825809478760, 28.3107604980469, 28.9388904571533, 29.5669898986816, 30.1950302124023, 30.8230400085449, 31.4510002136230, 32.0789184570313, 32.7067909240723, 33.3346290588379, 33.9624099731445, 34.5901603698731, 35.2178611755371, 35.8455200195313, 36.4731407165527, 37.1007118225098, 37.7282409667969, 38.3557281494141, 38.9831695556641, 39.6105690002441, 40.2379302978516, 40.8652381896973, 41.4925117492676, 42.1197395324707, 42.7469215393066, 43.3740615844727, 44.0011596679688, 44.6282081604004, 45.2552299499512, 45.8821907043457, 46.5091209411621, 47.1360015869141, 47.7628402709961, 48.3896293640137, 49.0163917541504, 49.6430892944336, 50.2697601318359, 50.8963813781738, 51.5229606628418, 52.1495018005371, 52.7759895324707, 53.4024391174316, 54.0288505554199, 54.6552085876465, 55.2815284729004, 55.9078102111816, 56.5340385437012, 57.1602287292481, 57.7863807678223, 58.4124794006348, 59.0385398864746, 59.6645584106445, 60.2905311584473, 60.9164695739746, 61.5423507690430, 62.1682014465332, 62.7939987182617, 63.4197616577148, 64.0454711914063, 64.6711502075195, 65.2967681884766, 65.9223632812500, 66.5478973388672, 67.1734008789063, 67.7988586425781, 68.4242706298828, 69.0496368408203, 69.6749725341797, 70.3002471923828, 70.9254913330078, 71.5506896972656, 72.1758422851563, 72.8009490966797, 73.4260177612305, 74.0510406494141, 74.6760177612305, 75.3009567260742, 75.9258499145508, 76.5507125854492, 77.1755065917969, 77.8002777099609, 78.4250030517578, 79.0496826171875, 79.6743087768555, 80.2989120483398, 80.9234466552734, 81.5479583740234, 82.1724166870117, 82.7968368530273, 83.4212188720703, 84.0455474853516, 84.6698379516602, 85.2940902709961, 85.9182891845703, 86.5424499511719, 87.1665725708008, 87.7906417846680, 88.4146728515625, 89.0386581420898, 89.6625976562500, 90.2864990234375, 90.9103622436523, 91.5341720581055, 92.1579513549805, 92.7816696166992, 93.4053573608398, 94.0289993286133, 94.6526031494141, 95.2761535644531, 95.8996734619141, 96.5231323242188, 97.1465606689453, 97.7699432373047, 98.3932800292969, 99.0165786743164]
    tem=[29.5799999237061, 29.5799999237061, 29.5799999237061, 29.5799999237061, 29.5699996948242, 29.5699996948242, 29.5599994659424, 29.5499992370605, 29.5000000000000, 29.4599990844727, 29.3999996185303, 29.3600006103516, 29.3500003814697, 29.3400001525879, 29.3299999237061, 29.3199996948242, 29.2900009155273, 29.2999992370605, 29.2900009155273, 29.2800006866455, 29.2800006866455, 29.2600002288818, 29.2500000000000, 29.2299995422363, 29.2299995422363, 29.2199993133545, 29.2000007629395, 29.1599998474121, 29.1100006103516, 29.0699996948242, 29, 28.9599990844727, 28.8999996185303, 28.8700008392334, 28.8299999237061, 28.7900009155273, 28.7700004577637, 28.7399997711182, 28.7099990844727, 28.6900005340576, 28.6800003051758, 28.6700000762939, 28.6499996185303, 28.6299991607666, 28.6200008392334, 28.5900001525879, 28.5699996948242, 28.5200004577637, 28.4799995422363, 28.4599990844727, 28.4500007629395, 28.4200000762939, 28.3999996185303, 28.3899993896484, 28.3799991607666, 28.3799991607666, 28.3500003814697, 28.3400001525879, 28.3199996948242, 28.2900009155273, 28.2500000000000, 28.2000007629395, 28.1599998474121, 28.1200008392334, 28.0599994659424, 28.0200004577637, 27.9699993133545, 27.9400005340576, 27.9200000762939, 27.8999996185303, 27.8700008392334, 27.8500003814697, 27.8199996948242, 27.7800006866455, 27.7299995422363, 27.6700000762939, 27.6499996185303, 27.6499996185303, 27.6299991607666, 27.6399993896484, 27.6399993896484, 27.6200008392334, 27.6299991607666, 27.6200008392334, 27.6200008392334, 27.6399993896484, 27.6200008392334, 27.6200008392334, 27.6200008392334, 27.6200008392334, 27.6200008392334, 27.6200008392334, 27.6200008392334, 27.6200008392334, 27.6200008392334, 27.6100006103516, 27.6200008392334, 27.6200008392334, 27.6299991607666, 27.6200008392334, 27.6200008392334, 27.6299991607666, 27.6200008392334, 27.6200008392334, 27.6299991607666, 27.6299991607666, 27.6299991607666, 27.6299991607666, 27.6299991607666, 27.6299991607666, 27.6299991607666, 27.6399993896484, 27.6399993896484, 27.6399993896484, 27.6399993896484, 27.6299991607666, 27.6299991607666, 36.0699996948242, 36.7999992370606, 36.7999992370606, 36.7999992370606, 36.7999992370606, 36.7999992370606, 36.7999992370606, 36.7900009155273, 36.2099990844727, 35.7599983215332, 35.2999992370606, 34.4599990844727, 33.9500007629395, 33.5400009155273, 33.1300010681152, 33.0800018310547, 32.6699981689453, 32.4700012207031, 32.3689994812012, 32.3499984741211, 32.2700004577637, 32.1800003051758, 32.0200004577637, 31.9699993133545, 31.9899997711182, 32.0699996948242, 31.7700004577637, 31.5599994659424, 31.4099998474121, 31.3299999237061, 31.2299995422363, 31.1599998474121, 31.1499996185303, 31.1599998474121, 31.0799999237061, 31.0400009155273]

    # tem=[25.4,27.5,27,26,25,23,22,22,21.5,21]
    month=3
    # kflagt=climatology_check(rlat, rlon, len(depth), depth, tem, maxim, zedqc, tmin, tmax, month)
    [kflagt,tmin_array,tmax_array]=climatology_check(rlat, rlon, len(depth), depth, tem, month)
    print(kflagt)

