# CODC Quality Control User Manual

Release v1.0

Author: Zhetao Tan (<font color=#0099ff><u>tanzhetao@mail.iap.ac.cn</u></font>) 

Contributor: Lijing Cheng, Viktor Gourestki, Yanjun Wang, Bin Zhang

Center for Ocean Mega-Science, Chinese Academy of Sciences (COMS/CAS)

Institute of Atmospheric Physics, Chinese Academy of Sciences (IAP/CAS)



## 1. Overview

The *in-situ* observations collected from the ocean are quality-heterogeneous. Decades of efforts have been dedicated to developing different manual or automatic quality control (QC) system to improve the quality and availability of ocean database, which is one of the basic tasks in many oceanic studies.

The goals of developing the automatic QC (AutoQC) is to provide a quality-homogeneous database, with reducing human-workload and time-consuming on manual QC as well as adapting the increasing volume of daily real-time data flow on observing system and large data centers. 

Here, we developed an AutoQC system (we refer to this procedure as **CODC-QC** system (Chinese Academy of Sciences (CAS) - Ocean Data Center (CODC) Quality Control system) to quality control the ocean *in-situ* observations. 

**This is the CODC-QC quality control user manual document for temperature *in-situ* data**. It describes four levels of quality control:

- The first level is CODC-QC performs a set of automatic checks that are not related to any variable measured during the profile. 
- The second level is CODC-QC performs three independent automatic checks that are related to the acceptable range of the measured value. 
- The third level is CODC-QC performs four independent automatic checks that  are related to the vertical structure (shape) of the measured profile. 
- The fourth level is a check that are applied only to profiles obtained by specific instruments. In this version, only XBT are available.

In this version, CODC-QC is only available for temperature observations. It covers all temperature data instrument types (e.g., Bottle, XBT, CTD, Argo etc.).   In the future, CODC-QC will extent to salinity observations and oxygen observations.

In this manual, the details of each QC check, especially the details of the parameter setting, is presented in Section 2. In addition, the method of how to install the CODC-QC in Python and getting started with CODC-QC is introduced in Section 3-4. The operator can consult this document to apply the CODC-QC according to their own needs.

## 2. Introduction of  CODC-QC

CODC-QC is an open source Python library to the quality control of ocean *in-situ* observations (e.g, temperature profiles, salinity profiles etc.). It was developed to reduce human-workload and time-consuming on manual quality control as well as adapt the increasing volume of daily real-time data flow on observing system and large data centers. 

> #### Why CODC-QC

- CODC-QC contains several QC checks that can be easily combined and tuned by users.
- CODC-QC provides many typical data interface for inputting raw data.
- The QC flags in CODC-QC are optional multiple categories, which depends on user's purposes.
- CODC-QC is a climatology-based automatic quality control algorithm. It is good at detecting bad data with paying an acceptable low price of sacrificing good data.
- The performance of CODC-QC has been meticulously analyzed and evaluated by comparing it with other international QC systems in  (Tan et al., 2022; under reivew)



### 2.1 CODC-QC checks

There are 14 QC checks for oceanic **profiles** in total.  The composition of CODC-QC is shown in Table 1.

<center>Table. 1 The composition of CODC-QC checks for temperature AutoQC. </center>

| Order |              Name  of checks              |                           Comments                           |
| :---: | :---------------------------------------: | :----------------------------------------------------------: |
|   1   |          Basic information check          | Check whether date, time, location are in  acceptable ranges. |
|   2   |         Sample level order check          | Check whether the depths are in a  monotonically increasing sample. |
|   3   |      Instrument maximum depth check       |      Check the profile based on instrument type  depths      |
|   4   |         Local bottom depth check          | Check whether  the deepest sampled level is larger than the bottom depth |
|   5   |            Global range check             |     Check whether the observations are in gross  errors.     |
|   6   |      Sea-water freezing point check       | Check whether  the observation is lower than the local freezing point temperature |
|   7   |     Local climatological range check      |    Check the outlier based on a local  climatology range     |
|   8   |           Constant value check            |        Check whether the profile exists stuck values         |
|   9   |                Spike check                | Check whether  the profile exists extremely outliers (spikes or 'bullseyes') |
|  10   |          Density inversion check          |    Check whether density increases with increasing depth     |
|  11   |          Multiple extrema check           | Check whether the profile is in a big number  of temperature extremes |
|  12   |      Global vertical gradient check       | Check whether the observations are in a sharp  increase/decrease. |
|  13   | Local gradient climatological range check | Check the  vertical gradient of the profiles based on a local gradient climatology range |
|  14   |         Instrument specific check         | Only checks in  XBT profiles related to XBT wire stretch, leakage, hit bottom, wire break,  etc. |

Here we show the details (including parameter settings) for each check below.

####   2.2.1 Basic information check

This test identifies the date/time/location of the selected profile based on the general information. All observations in the selected profile are **flagged as 1** when the metadata falls outside the general information range. For example: 

- the year should be fell inside the range [1750, 2022]
- the month should be fell inside the range [1, 12]
- the latitude should be fell inside the range [-83, 90] 
- the longitude should be fell inside the range [-180, 180] or [0 360]
- the number of depth records should be the same with the number of  temperature records.

Additionally, the depth records should be greater or equal to zero (if down is the positive value). If not, observations that fall within the negative depth records **are flagged as 1**.

The directory of source codes for this check is :  `/qc_models/check_aqc_01.py`

####  2.2.2 Sample levels order check

This test identifiers whether the sample depth levels are placed in increasing order. If a depth measurement is not an increasing depth value, this observations are **flagged as 1.**

The directory of source codes for this check is :  `/qc_models/check_aqc_02.py`

#### 2.2.3 Instrument maximum depth check

Each instrument type is designed to operate within a certain depth range. For example, MBT cannot exceed depth below 320 meters, CTD cannot withhold depth above 2 meters, and the maximum sample depth for XBT probes is limited by the length of the wire which depends on the probe type. If a depth record falls outside the nominal depth range for the instrument type, the values beyond the range are **flagged as 1**.

Here, CODC-QC sets the type-dependent range is:

- CTD: 2m - 8000m (depth records above 2m are all flagged)
- MBT: 0m - 320m
- XBT: 3m - 2200m  (depth records above 3m are all flagged)
- OSD, CTD, XCTD: 0m-9000m
- PFL (Argo): 0m - 6050m
- APB: 0m - 1200m

The directory of source codes for this check is :  `/qc_models/check_aqc_03.py`

#### 2.2.4 Local bottom depth check

This check identifies whether the deepest sampled level is larger than the bottom depth. The latest version of global 0.5 arc-second resolution digital General Bathymetric Chart of the Oceans (GEBCO) provides the estimate of the local ocean bottom depth (Tozer et al. 2019). Values exceed the bottom depth are **flagged as 1**.

As the digital bathymetry is not error-free due to the uncertainty in the profile location, a small tolerance (`dtol`) as a function of bottom depth (`bottom_depth`) is added to the local ocean bottom depth  as followed:

> for the profile located north of 60S:

$$
dtol= 15.0+bottom\_depth * 0.05 (bottom\_depth < 1000m)
\\
dtol = 80 (bottom\_depth >= 1000m)
$$
> For the profile located south of 60S:

$$
dtol= 270.0 - bottom\_depth * 0.37
$$

The GEBCO records are stored in the external files located at  `<CODC-QC_location>/CODC-QC/background_field/gebco_2021_15arcsecond.npz`

The directory of source codes for this check is :  `/qc_models/check_aqc_04.py`

####  2.2.5 Global range check

This test identifiers whether the observation are in gross error based on the temperature depth-dependent (upper and lower) threshold (range). This range is statistically analyzed based on all available temperature profiles and constructed using the upper and the lower boundaries of the 0.5% and 99.5% quantiles respectively. Values exceed the overall depth-dependent range are **flagged as 1**. The global depth-dependent temperature range is shown in Table 1.

<center>Table 1. The global temperature (℃) depth-dependent thresholds used in the global crude range check
</center>

| Depth (m) | Lower bounds | Upper bounds | Depth (m) | Lower bounds | Upper bounds |
| :-------: | :----------: | :----------: | :-------: | :----------: | :----------: |
|     1     |    -1.948    |    34.000    |   1050    |    -1.184    |    11.734    |
|     3     |    -1.952    |    34.000    |   1100    |    -1.177    |    11.593    |
|     5     |    -1.980    |    33.000    |   1150    |    -1.150    |    11.526    |
|    10     |    -1.988    |    33.000    |   1200    |    -1.141    |    11.478    |
|    15     |    -1.988    |    32.000    |   1250    |    -1.148    |    11.366    |
|    20     |    -1.980    |    31.000    |   1300    |    -1.166    |    11.183    |
|    25     |    -1.977    |    30.952    |   1350    |    -1.136    |    10.865    |
|    30     |    -1.977    |    30.769    |   1400    |    -1.131    |    10.384    |
|    35     |    -1.975    |    30.688    |   1450    |    -1.131    |    10.020    |
|    40     |    -1.972    |    30.641    |   1500    |    -1.120    |    9.428     |
|    45     |    -1.973    |    30.626    |   1550    |    -1.111    |    8.474     |
|    50     |    -1.970    |    30.510    |   1600    |    -1.102    |    7.865     |
|    55     |    -1.964    |    30.537    |   1650    |    -1.104    |    7.339     |
|    60     |    -1.959    |    30.503    |   1700    |    -1.098    |    6.875     |
|    65     |    -1.958    |    30.441    |   1750    |    -1.100    |    6.428     |
|    70     |    -1.955    |    30.390    |   1800    |    -1.099    |    6.013     |
|    75     |    -1.958    |    30.302    |   1850    |    -1.099    |    5.694     |
|    80     |    -1.959    |    30.198    |   1900    |    -1.105    |    5.394     |
|    85     |    -1.960    |    30.092    |   1950    |    -1.115    |    5.122     |
|    90     |    -1.957    |    29.992    |   2000    |    -1.183    |    5.102     |
|    95     |    -1.958    |    29.875    |   2100    |    -1.179    |    4.940     |
|    100    |    -1.966    |    29.750    |   2200    |    -1.170    |    4.168     |
|    110    |    -1.962    |    29.534    |   2300    |    -1.180    |    3.892     |
|    120    |    -1.963    |    29.335    |   2400    |    -1.186    |    3.727     |
|    130    |    -1.962    |    29.028    |   2500    |    -1.177    |    4.058     |
|    140    |    -1.960    |    28.671    |   2600    |    -1.169    |    3.495     |
|    150    |    -1.961    |    28.327    |   2700    |    -1.166    |    3.430     |
|    160    |    -1.962    |    27.794    |   2800    |    -1.171    |    3.461     |
|    170    |    -1.964    |    27.314    |   2900    |    -1.177    |    3.265     |
|    180    |    -1.963    |    26.703    |   3000    |    -1.166    |    3.202     |
|    190    |    -1.963    |    26.014    |   3100    |    -1.177    |    3.125     |
|    200    |    -1.966    |    25.063    |   3200    |    -1.184    |    3.110     |
|    220    |    -1.965    |    23.047    |   3300    |    -1.148    |    3.014     |
|    240    |    -1.965    |    21.690    |   3400    |    -1.150    |    3.016     |
|    260    |    -1.961    |    20.688    |   3500    |    -0.891    |    2.980     |
|    280    |    -1.967    |    19.910    |   3600    |    -0.869    |    2.818     |
|    300    |    -1.970    |    19.500    |   3700    |    -0.686    |    2.758     |
|    320    |    -1.971    |    19.230    |   3800    |    -0.671    |    2.643     |
|    340    |    -1.975    |    19.075    |   3900    |    -0.725    |    2.640     |
|    360    |    -1.977    |    18.947    |   4000    |    -0.777    |    2.607     |
|    380    |    -1.977    |    18.809    |   4100    |    -0.778    |    2.615     |
|    400    |    -1.976    |    18.670    |   4200    |    -0.660    |    2.616     |
|    425    |    -1.979    |    18.498    |   4300    |    -0.570    |    2.591     |
|    450    |    -1.981    |    18.322    |   4400    |    -0.614    |    2.618     |
|    475    |    -1.973    |    18.181    |   4500    |    -0.648    |    2.604     |
|    500    |    -1.969    |    18.023    |   4600    |    -0.571    |    2.572     |
|    525    |    -1.963    |    17.871    |   4700    |    -0.578    |    2.574     |
|    550    |    -1.965    |    17.668    |   4800    |    -0.557    |    2.559     |
|    575    |    -1.951    |    17.445    |   4900    |    -0.558    |    2.572     |
|    600    |    -1.950    |    17.179    |   5000    |    -0.512    |    2.587     |
|    625    |    -1.938    |    16.875    |   5100    |    -0.461    |    2.579     |
|    650    |    -1.934    |    16.512    |   5200    |    -0.442    |    2.580     |
|    675    |    -1.927    |    16.110    |   5300    |    -0.437    |    2.568     |
|    700    |    -1.921    |    15.693    |   5400    |    -0.430    |    2.485     |
|    750    |    -1.906    |    14.740    |   5500    |    -0.387    |    2.501     |
|    800    |    -1.890    |    13.778    |   5600    |    -0.373    |    2.507     |
|    850    |    -1.437    |    12.844    |   5700    |    -0.308    |    2.508     |
|    900    |    -1.246    |    12.204    |   5800    |    -0.300    |    2.486     |
|    950    |    -1.226    |    11.919    |   5900    |    -0.300    |    2.500     |
|   1000    |    -1.196    |    11.707    |   6000    |    -0.300    |    2.500     |

Specially, this check is not performed in the Mediterranean Sea, the Red Sea, the Gulf of Mexico (below 2000m) because these regions having specific thermohaline structure, which are quite different from the open ocean.

The directory of source codes for this check is :  `/qc_models/check_aqc_05.py`

#### 2.2.6 Sea-water freezing point check

As sea water does not freeze (except at the polar sea surface), this check aims at determining whether the temperature observations are cooler than the freezing point temperature defined by UNESCO-IOC (1983) as followed:
$$
T_f=-0.0575*S+1.710523E^{-3} * S^{\frac{3}{2}}-2.154996E^{-4}*S^2-7.53E^{-4}* P
$$
here,   `Tf`  is the freezing point temperature in degrees Celsius, *S* *i*s the salinity in PSU within [27,35], and *P* *i*s the pressure in decibars. If the accompanying observed salinity profile is not available (e.g., for XBT, MBT, APB, GLD temperature profiles), the IAP monthly climatological salinity on a 1-degree box was used (Cheng et al. 2020). Values smaller than  `Tf` are **flagged as 1**. 

The directory of source codes for this check is :  `/qc_models/check_aqc_06.py`

#### 2.2.7 Local climatological range check

This check is identical to the global crude range check in Section 2.2.5, but with temperature climatological ranges defined locally. This check aims at determining whether the observed values fall within an acceptable local climatological temperature range in a local scale. The local climatological range represents the maximum amplitude of water mass variation. Here, the **IAP-T-range** are used as the local climatological temperature range. The upper boundary `(Tmax)` and the lower boundary `(Tmin)`defined by the 0.5% and 99.5% quantile are monthly constructed with all observations on a 1-degree box. 

Additionally, a long-term trend (shift) of the climatological bounds is considered in a human-induced warming oceans by adding a linear coefficient to the IAP-T-range. That is, **a time-varying IAP-T-range is used** in this check rather than a constant IAP-T-range. The time-varying local climatological temperature threshold is defined as followed:
$$
T'_{max} = T_{max} + Year* |k_{max}|
\\
T'_{min} = T_{min} - Year*|k_{min}|
$$
in which, `kmax` and `kmin` is the long-term trend of the 99.5% and 0.5% quantile over past 60 years (i.e., the shift of the climatological bounds) in each 1-degree box at each standard level, estimated by linearly fitting the quantiles defined by successive 20-year observations of 1941-1960, 1951-1970, 1961-1980, 1971-1990, 1981-2000, 1991-2010, 2001-2021. `Year` is the year (ranging from 1940-now) of observations. 

For a temperature observation (T) in level *k*, value falls outside the local monthly depth-dependent range are **flagged as 1** following the Equation below. 
$$
T_k  ∉[T'_{min}(k,month,lat,lon), T'_{max}(k,month,lat,lon)]
$$
Details of the construction of **IAP-T-range** is shown in Tan et al., 2022 (under review).

The  monthly IAP-T-range climatology field is saved in   `<CODC-QC_location>/CODC-QC/background_field/IAP_T_range.mat`.

The monthly linear coefficients (i.e., `kmax` and `kmin`) for the time-varying IAP-T-range is saved in `<CODC-QC_location>/CODC-QC/background_field/IAP_T_range_kmax_kmin.mat`

The directory of source codes for this check is :  `/qc_models/check_aqc_7.py`

#### 2.2.8 Constant value check

This identifies temperature profile for stuck value or unrealistically thick thermostad. It is referred (Gourestki, 2018). These test includes two parameters:

H - the minimal thickness of the layer within which all measurements shows exactly the same value. H is set to be 300 meters (400 meters in the polar region grater than 65N or smaller than 65S).

N - the number of levels showing exactly the same value within the layer H.

The tuning parameter N is assumed to be instrument-type dependent:

- Nansen casts (BOT): 10
- CTD, XCTD: 50
- PFL (Argo): 20
- XBT: 20
- APB: 20
- Other instrumentations: 7

All measurements detected as stuck value or within the unrealistic thick thremostad  (H) are **flagged as 1.**

The directory of source codes for this check is :  `/qc_models/check_aqc_08.py`

#### 2.2.9 Spike check

This check identifies the temperature spike on the selected profiles, which is similar to Gourestki, 2018. For each triple of temperature values on neighboring depth levels (*k, k+1, k+2*), the spike (*S*) is defined as:
$$
S_1 = |T_{k1}-(T_k+T_{k+2})*0.5|
\\
S_2 = |(T_{k+2}-T_k)*0.5|
\\
S=S_1 - S_2
$$
The ***S*** is compared to be a tun-able depth-dependent thresholds ***Smax***:

$$
S_{max}=\begin{cases}  4, \quad 0<depth<1000m   \\  3, \quad 1000<depth<2000m \\ 2, \quad depth>2000m            \end{cases}
$$
if $S>~max$, the values at level k+1 is detected as spike and **flagged as 1.** 

Specially, the spike test is not performed for the observed levels in big vertical gaps. Following thresholds `(dmax or emax)`are applied:

$$
Z_{k+2} - Z_k > d_{max}
\\
Z_{k+2} - Z_{k+1} > e_{max}
\\
Z_{k+1} - Z_k > d_{max}
$$
where
$$
d_{max}=50+Z_k /10
\\
e_{max}=d_{max}*0.5
$$
The directory of source codes for this check is :  `/qc_models/check_aqc_09.py`

#### 2.2.10 Density inversion check

Ocean forms stratified layers.This check identifies whether the density increases with increasing depth. The density is calculated from absolute salinity and conservative temperature by using the computationally-efficient 75-term expression (Roquet et al. 2015). 

Similary with WOD-QC (Garcia et al., 2018), the density inversion is calculated by using the one-side differential: the density difference is calculated as displaced sample's density minus the shallower sample's density. Then, the density difference is divided by the depth difference between adjacent levels unless the difference is less than 3 meters, in which case a difference of 3 meters is used.

If density inversion at level *k* occurs and the inversion beyond a depth-dependent threshold (the threshold is the same as WOD-QC), both temperature and salinity at level *k* were **flagged as 1**.

The global depth-dependent density inversion threshold is: 

- For observations with a sampling depth less than 30 meters, the inversion threshold is ``3x10^(-5) g/cm^3``
- For observations with a sampling depth greater than 30 meters but less than 400 meters, the inversion threshold is ``2x10^(-5) g/cm^3``
- For observations with a sampling depth greater 400 meters, the inversion threshold is ``1x10^(-6) g/cm^3``

Note that this check is not performed if the salinity observations are not available (e.g., XBT observations).

The directory of source codes for this check is :  `/qc_models/check_aqc_10.py`

#### 2.2.11 Multiple extrema check

This check identifiers profiles with unrealistically big number of local temperature extrema on neighboring depth levels (***k, k-1, k+1***). An extreme is defined if:

$$
T_k - T_{k+1} < d  \quad and \quad T_k-T_{k-1}<d
\\
d=0.5
$$
The thresholds ***d*** has considered the measurement precision or the typical size of the micro-scale temperature inversions.  In CODC-QC, ***d*** is subjectively set to be 0.5℃ (depends on the frequency histogram). 

Values exceed the continuous temperature extreme are **flagged as 1**.

The directory of source codes for this check is :  `/qc_models/check_aqc_11.py`

#### 2.2.12 Global vertical gradient check

This check identifies temperature observations for which its vertical temperature gradient exceeds the overall depth-dependent gradient climatological range, which is similar to the global crude range check for temperature in Section 2.2.5. 

CODC-QC calculates the temperature gradient of a profile ( $(∇T)_k$) at level *k* using central differences as follows:
$$
if \quad (Z_{k+1}-Z_{k-1}≥10m):\quad (∇T)_k=\frac{δT}{δZ}=\frac{(T_{k+1}-T_{k-1})}{(Z_{k+1}-Z_{k-1})}
\\
if \quad (Z_{k+1}-Z_{k-1}<10m): \quad \begin{cases} (∇T)_k=\frac{δT}{δZ} \\ δZ=Z_{k+N_2}-Z_{k-N_1}>10m \\   δT=\frac{1}{N_2} ∑_{i=k}^{N_2}T_i - \frac{1}{N_1}∑_{i=k-N_1}^kT_i         \end{cases}
$$
If  depth interval between levels ***k-1*** and ***k + 1*** are less than 10 meters, CODC-QC will automatically choose the smallest value of `N1` and `N2` which corresponds to the vertical gap greater than 10m and then applys the mean gradient calculation. The definition of 10m is mainly due to in this study, CODC-QC does not focus on the micro-structured natural vertical noises, which is often captured by high-resolution profiles that its vertical gaps are less than 10m.

We apply different gradient ranges depending on the profile vertical resolution.

Here, the global overall temperature vertical gradient range is statistically analyzed based on all available temperature gradient profiles and constructed using the upper and the lower boundaries of the 0.5% and 99.5% quantiles respectively. The temperature at level *k* for which the vertical gradient falls outside the global gradient range is **flagged as 1**.

For more details of gradient calculations and gradient climatology range, please refer to Tan et al., 2023

The directory of source codes for this check is :  `/qc_models/check_aqc_12.py`	

#### 2.2.13 Local gradient climatological range check

This check is identical to the global gradient check in Section 2.2.11 but with gradient climatological ranges defined locally similar to the local climatology check for temperature described in Section 2.2.7. 

The method for calculating the vertical gradient profiles is the same as methods used in Section 2.2.12.

Here, the **IAP-TG-range** in different vertical gaps are used as the local climatological vertical gradient range. The upper boundary and the lower boundary of the 0.5% and 99.5% quantiles are monthly constructed with all vertical gradient profiles on a 1-degree box in different vertical interval gaps (δZ) within 10m to 160m . 

For a temperature observation (T) in level *k*, its corresponding vertical gradient value falls outside the local monthly depth-dependent range are **flagged as 1** following th eaution below:
$$
(∇T)_k  ∉[TG_{min}(δZ,k,month,lat,lon),\quad TG_{max}(δZ,k,month,lat,lon)]
$$
Details of the construction of IAP-TG-range is show in the Tan et al., 2022 (under reivew). 		

The  monthly IAP-TG-range climatology file is saved in   `<CODC-QC_location>/CODC-QC/background_field/IAP_TG_range.mat`.

The directory of source codes for this check is :  `/qc_models/check_aqc_12.py`

#### 2.2.13 Instrument specific check (XBT)

In the highly non-homogeneous archive like WOD, spurious temperature profiles often exhibit features which are characteristic only to specific instrumentations. These features can be attributed to specific problems encountered during the data acquisition. 

For XBT profiles, errors such as wire stretch, wire insulation damage, leakage problems and bottom hit can be linked to instrument malfunctions. Previous studies show that if a temperature measurement at a specific level is identified as one of these problems, the measurements below this level are all flagged as bad (Barton and Gonzalez 2016). 

Therefore, this check aims at identifying the XBT profile that whether the number of rejected observations starting at level *k*, which are judged to fail the local gradient climatology range in the local gradient climatology check (Section 2.2.12).

This check includes two parameters:

N - the minimum number of 'consecutive' rejected data starting at level *k*. 'Consecutive' means all data is rejected within a certain depth range.

T - the minimum number of  'consecutive' rejected data groups on a selected profile.

The tuning parameter N and T are assumed to be probes-depth-dependent:

- For the XBT observations measured by T4/T6 probe types:   `N` set to be 6 empirically, `T` set to be 2 if maximum observed depth lower than 400m and set to be 1 if maximum observed depth greater than 400m.
- For XBT observations measured by T7/DB probe types: `N` set to be 6 empirically, `T` set to be 3 within depth above 800m and set to be 1 if depth below 800 meters.

If fails the thresholds, all observations below the level *k* will be **flagged as 1**. 

In the current CODC-QC version, this check is only available for the XBT profiles.

### 2.3 CODC-QC flag

CODC-QC defines the quality control flag based on the criteria below:

The QC flag is dichotomic for each check at each observed depth level, **with 0 denotes the acceptable (good) value and 1 denotes the rejected (bad) value**.  

Additionally, a **final flag** with all checks are provided for temperature at each observed depth: If the observation are detected as outlier in any check (more than one check), then the **final flag** will be set as 1, otherwise set as 0.

For example in the Table 1, since CODC-QC has 14 checks in total, therefore, the CODC-QC will output corresponding flag result from each check **(Check 1 - Check 14)** for each observed depth. In addition, a final flag will also output for each observed depth. This can help the user know what happen in each check. If an observation is detected as outlier in too many checks, we will have high confidence to know this observations are definiately bad value. Conversely, if an observation is flagged as outlier in only one check, we should have cautious to discard this observations. **In conclusion, the flags are optional multiple categories, which depends on user's purposes.**

> ***Suggestions***: If user wants to retain good data as much as possible in paying the price of having some bad data, we recommend it to cautiously double-check each flag in each check.  On the contrary, if user wants to discard bad data as much as possible, in spite of they are willing to pay the price of loosing some small number of good data, **we recommend you to use the FInal Flag and delete all the data flagged as 1**. 

<center>Table 1. An example of CODC-QC flag for a typical temperature profile</center>

| Depth (m) | Temperature (^o^C) |       Check 1- Check 14       | Final flag |
| :-------: | :----------------: | :---------------------------: | :--------: |
|    2.5    |        32.7        | [0,0,1,0,0,0,0,0,1,0,1,0,0,0] |     1      |
|     5     |        29.5        | [0,0,1,0,0,1,1,1,1,0,1,1,0,1] |     1      |
|   60.7    |        26.4        | [0,0,0,0,0,0,0,0,0,0,0,0,0,0] |     0      |
|   ....    |        ....        |             ....              |    ....    |
|   512.5   |        7.8         | [0,0,0,0,0,0,0,0,1,0,0,0,0,0] |     1      |

​	                     

## 3. Installation 

#### 3.1 Requirement packages

+ Python 3.7（>=3.7 is OK, but 3.7 is strongly recomended)
+ numpy (>= 1.19.1)
+ scipy (>= 1.4.1)
+ netCDF4 (>= 1.5.5.1)
+ h5py (>= 2.10.0)
+ gsw (>= 3.4.0)

> Computer Memory: >16GB is obligatory.

#### 3.2 Installing CODC-QC

<b> Step1: Using pip to quick install</b>

If you don’t already have **PIP** running on your machine, first you need to **install pip**, then you can run:

```shell
pip install CODCQC
```

please make sure <b> PIP </b> fits your version of python3.X. In some machines, you should use `pip3 install CODC-QC` because **"pip"** may be linked to python2.X 

>  if you use the [conda](http://conda.io/) package manager `conda install -c conda-forge CODCQC`

Then you will wait for **serveral minutes** to install the package.

> If you **can not** install the package automatically, you can install it manually in the terminal by run: `pip install CODCQC-1.0-py3-none-any.whl `

***The files `CODCQC-1.0-py3-none-any.whl ` could be download [here](http://www.ocean.iap.ac.cn/ftp/cheng/CODC-QC/) manually.***



<b> Step2: Downloading external background files </b>

> **Specially, this step could be skipped if you installed CODC manually.**

In this step, you should only go to the CODCQC installing directory to check whether the external files are existed:

```sh
pip show CODCQC 
```

or

``` shell
pip show CODCQC | grep Location
```

then you will find the installed location `<CODC-QC_location>`.

Then, go to the installed directory:

```shell
cd <CODC-QC_location>
cd CODC-QC/background_field
ls -l
```

**If you find these 6 external files below, then you can go to Step 3.**

- IAP_T_range.mat
- IAP_TG_range.mat
- Gebco_2021_15arcsecond.npz
- IAP_T_range_kmax_kmin.mat
- climatology_Savg_IAP41_1955_2020.mat
- regions_mask.mat

> **If you can't find enough files or if the size is not matched, you should download these files manually from [Ocean website of IAP](http://www.ocean.iap.ac.cn)**, and then save these files in the path `<CODC-QC_location>/CODCQC/background_field`



The tree directory of CODC-QC Python Package is shown in Figure 2. It includes 4 directories. The quality control main program is `AutoQC_main.py` in the root directory `<CODC-QC_location>`. The demos are in `<tests>` directories.

![tree-CODCQC](/Users/zqtzt/Downloads/tree-CODCQC.png)

 <center> Fig. 2.  The tree directory of CODCQC Python Package.</center>

<b> Step3: Making a first and easiest QC test </b>

​	We provide a **demo**. Now, you can make a first and easiest QC test to check whether the CODCQC package works well.

​    Launch your Python, then:

```python
### import the package
### you will wait for about 10-30 seconds to read the external files.
import CODCQC
### run the demo (Example1_single_cast_AutoQC.py)
from CODCQC.tests import Example1_single_cast_AutoQC
```

If return the following result, congratulations!! The CODC-QC package works well.

```
start reading GEBCO depth file
start reading temperature climatology field
start reading linear coefficient for time-varying IAP-T-range
start reading temperature gradient climatology field
start reading salinity climatology field
Depth is: [0.0, 5.598, 7.8, 11.2, 14.0, 16.6, 20.0, 21.299]
Temperature is: [9.1, 8.7, 8.3, 7.2, nan, 5.1, 4.4, 4.5]
Temperature QC result is: [1, 0, 0, 0, 1, 0, 0, 0]
QC result of each check is:
Basic infomation check is:  [0, 0, 0, 0, 0, 0, 0, 0]
Sample levels order check is:  [0, 0, 0, 0, 0, 0, 0, 0]
Instrument maximum depth check is:  [1, 0, 0, 0, 0, 0, 0, 0]
Local bottom depth check is:  [0, 0, 0, 0, 0, 0, 0, 0]
Global range check is:  [0, 0, 0, 0, 1, 0, 0, 0]
Sea-water freezing point check is:  [0, 0, 0, 0, 0, 0, 0, 0]
Local climatological range check is:  [0, 0, 0, 0, 0, 0, 0, 0]
Constant value check is:  [0, 0, 0, 0, 0, 0, 0, 0]
Spike check is:  [0, 0, 0, 0, 0, 0, 0, 0]
Density inversion check is:  [0, 0, 0, 0, 0, 0, 0, 0]
Multiple extrema check is:  [0, 0, 0, 0, 0, 0, 0, 0]
Global vertical gradient check is:  [0, 0, 0, 0, 0, 0, 0, 0]
Local gradient climatological range check is:  [0, 0, 0, 0, 0, 0, 0, 0]
Instrument specific type (XBT) check is:  [0, 0, 0, 0, 0, 0, 0, 0]
```

Now, you can get started with CODC-QC!

## 4. Getting Started with CODC-QC

### 4.1 Data input from WOD netCDF files

World Ocean Database (WOD) is the most famous ocean database in the world. One of the most important uses of this package is to quality control of WOD *in-situ* observation data (only temperature profile is available now, the QC for salinity profile would be upgrade in the next version). Thus, an example for WOD18 quality control by using data input from netCDF files is provided in this package.

Please refer the file `<CODC-QC_location>/tests/Example2_WOD_netCDF_AutoQC.py`

```python
### import relevant packages
import CODCQC as CODCQC
import CODCQC.CODCQC_main as CODCQC_main
from CODCQC.util import IO_functions
from CODCQC.util import print_stat
import numpy as np

def main(file_path,makeTemperatureQC=True,makeSalinityQC=False):
    qc = CODCQC_main.QualityControl()  

    # the input folder include WOD18 netCDF file
    files = IO_functions.getFiles(file_path, '.nc')

    import time
    t1=time.time()
    myflagt_all = []
    kflagt_checks_all = []
    for file in files:
        print(file)

        # Read variables from WOD18 netCDF file
        # Handle:f  tempeature:tem Depth:depth  metadata:meta
        [f, tem, sal, depth, meta] = IO_functions.read_WOD(file)
        meta.gebcodepth=qc.get_gebcodepth(meta)
        
        # make COMS-AutoQC v1.0 check
        # make Temperature QC
        if(makeTemperatureQC==True):
            [myflagt, kflagt_T_checks] = qc.check_T_main(tem, depth, meta)
            # save the final QCflag
            myflagt_all.append(myflagt)
            kflagt_checks_all.append(kflagt_T_checks)  #make statistics
            # write QCflag to netCDF file
            f = IO_functions.write_nc_tempQC(f, myflagt)
                
        # close netCDF file
        f.close()

    # if you like, you can print the detail statsitcal results to the txt file
    if(makeTemperatureQC==True):
        print_stat.print_T_flag_txt(myflagt_all,kflagt_checks_all)

    t2=time.time()
    print('time cost: '+str(t2-t1))
```

If you want to run this example, please change the working directory to `<CODC-QC_location>/tests/`, and then run this example.

When it finished, a variable `Temperature_CASflag` will be added into the netCDF file . The dimension of this variable is corresponding to the `Temperature`. You can check the netCDF files in `<CODC-QC_location>/tests/WOD18_netCDF_temp_data`.

> Actually, *in-situ* observation data saved as netCDF files could use this demo to quality control,**BUT** **you should follow the criteria below:**

+ The netCDF file should include the following variables: Temperature, Depth, time, latitude, longitude, instrument type
+ The variables should strictly follow the names  *(case sensitive)* below in order to corresponding to the function `read_WOD_from_NC.read_WOD()`
  + <font color=#0099ff> **Temperature** </font>:  'Temperature'
  + <font color=#0099ff> **Depth** </font>: 'z'
  + <font color=#0099ff> **time** </font>: 'time'
  + <font color=#0099ff> **latitutde** </font>: 'lat'
  + <font color=#0099ff> **longitude** </font>: 'lon'
  + <font color=#0099ff> **Instrument type** </font>: 'dataset'  (should be consistent with WOD code table: https://www.ncei.noaa.gov/access/world-ocean-database/CODES/wod-datasets.html )


> If your netCDF files do not include these variables name, you can read by yourself instead of using function `read_WOD_from_NC.read_WOD()`. Otherwise you can manually modify the function `read_WOD_from_NC.read_WOD()` to fit the format of your own netCDF files.

### 4.2 Data input from TXT file 

In this package, we also provide a method by inputting data from the text file (*.txt). Please refer to the example: `<CODC-QC_location>/tests/Example3_txt_AutoQC.py`

You should only give 3 input variables to the QC check main function `check_profileQC_main()`: <font color=#0099ff> **depth,tem,meta** </font>

+ <font color=#0099ff> **depth** </font>: 1-dimension array or list for depth value

+ <font color=#0099ff> **tem** </font>: 1-dimension array or list for temperature value

+ <font color=#0099ff>  **meta** </font>: **a class object** with metadata attributes (include meta.lat, meta.lon, meta.levels, meta.year, meta.month, meta.day, meta.typ3)

If value is missing, you can use `np.nan` or use `9999` to set it (the recommended option is setting as NaN value. i.e., `np.nan`)

**An example input TXT file is provided in** `<CODC-QC_location>/tests/Example3_txt_input.txt`

The *.txt input files should have <font color=#0099ff> **sequential arrangement of each profile (cast)** </font>. The first line is metadata information, then followed by the observed value with two columns: the first column is depth value, the second column is temperature value at each observed depth.

```python
import CODCQC.CODCQC_main as CODCQC_main
from CODCQC.util import IO_functions
from CODCQC.util import print_stat
from CODCQC.util import CODCQC_constant as const
import numpy as np

makeTemperatureQC=True
makeSalinityQC=False

qc = CODCQC_main.QualityControl()

txt_file='./Example2_txt_input.txt'
[depth_all,tem_all,sal_all,meta_list]=IO_functions.read_data_from_TXT(txt_file)

num_prof=len(tem_all)
myflagt_all=[]
kflagt_checks_all=[]

for i in range(num_prof):
    print(i)
    depth=depth_all[i]
    tem=tem_all[i]
    sal=sal_all[i]
    meta=CODCQC_main.metaData()
    meta.typ3=meta_list[i][1]
    meta.year=int(meta_list[i][2])
    meta.month=int(meta_list[i][3])
    meta.day=int(meta_list[i][4])
    meta.lat=float(meta_list[i][5])
    meta.lon=float(meta_list[i][6])
    meta.levels = len(depth)
    meta.gebcodepth = qc.get_gebcodepth(meta)
    #### Now, one profile(cast) has been read
    # print("Depth is:", depth)
    # print("Temperature is:", tem)

    # make CODC-AutoQC v1.0 check;  myflagt is the final QC flag combined with all checks; kflagt_checks is the QC flag for each seperated check
    # make Temperature QC
    if (makeTemperatureQC):
        [myflagt, kflagt_T_checks] = qc.check_T_main(tem, depth, meta,sal)
        myflagt_all.append(myflagt)
        kflagt_checks_all.append(kflagt_T_checks)  ###make statistics

#### write txt file
output_file='./Example3_txt_output.txt'
IO_functions.write_QCflag_to_txt_T(output_file,depth_all,tem_all,meta_list,myflagt_all)
print('WRITING FLAG is finished: '+output_file)

# if you like, you can print the detail statistical results to the txt file
if (makeTemperatureQC == True):
    print_stat.print_T_flag_txt(myflagt_all, kflagt_checks_all)
```

Run this demo, you can get the example of how to use TXT files as the input method, then get the output quality flag in TXT format.

When it finished, the QC flag will be output as a TXT file `./Example2_txt_output.txt` and a TXT files recording the statistical results will also be output in the path `./`.

**If you want to use txt file as the input method, Please strictly follow the storage format of the sample TXT file ("./util/Example_txt_inpu.txt") by following below criteria:**

+ The first line is the meta-data informaiton.  For exmaple:

   "HH CTD 2013 3 27 20.495 120.467“

  with the meaning of [Handle identification, instrument type, year, month, day, lat, lon] respectively.

  **NOTE**: instrument type is strictly consistent with WOD code table: https://www.ncei.noaa.gov/access/world-ocean-database/CODES/wod-datasets.html  in three characters

+ Begins with the second line: the first column is depth value, the second column is temperature value at each corresponding depth. 
+ When observed values are finished, then begins with the second profile....

### 4.3 Data input from the MATLAB (*.mat) file

In this package, we also provide a method by inputting data from the MATLAB file (*.mat). Please refer to the example: `<CODC-QC_location>/tests/Example4_mat.py`

The MATLAB sample file is stored in `<CODC-QC_location>/tests/WOD18_mat_temp_data/`

**An example is provided in** `<CODC-QC_location>/tests/Example4_mat.py`

> Run this example and when it finishes, the `CODCQC_myflagt` (denotes the final QC flag for each observed level) and `CODCQC_myflagt_checks` (denotes QC flag for each QC check for each observed level) will be written into the sample MATLAB file.

### 4.4 Data input manually

You can easily use this package to quality control of your selected profiles.

#### 4.4.1 One-time execution of all AutoQC checks

Here is an example of how to make the CODC AutoQC program manually with a single oceanic observation profile (Now only Temperature are available).

You should only give 3 input variables to the QC check main function `check_profileQC_main()`: <font color=#0099ff> **depth,tem,meta** </font>

+ <font color=#0099ff> **depth** </font>: 1-dimension array or list for depth value

+ <font color=#0099ff> **tem** </font>: 1-dimension array or list for temperature value

+ <font color=#0099ff>  **meta** </font>: **a class object** with metadata attributes (include meta.lat, meta.lon, meta.levels, meta.year, meta.month, meta.day, meta.typ3)

  If value is missing, you can use `np.nan` or use `9999` to set it (the recommended option is setting as NaN value. i.e., `np.nan`)

```python
import CODCQC
from CODCQC import CODCQC_main
from CODCQC.util import CODCQC_constant as const
import numpy as np

qc = CODCQC_main.QualityControl()  #create a quality control object

depth = [0.0, 5.598, 7.800, 11.200, 14.000, 16.600, 20.000, 21.299]    #1-dimension array or list for depth value
tem = [9.1, 8.7, 8.3, 7.2, np.nan , 5.1, 4.4, 4.5]  #1-dimension array or list for temperature
print("Depth is:",depth)
print("Temperature is:",tem)


#create object to set metadata of a profile(cast)
meta=CODCQC.metaData()
#put metadata attributes into the meta object
meta.lat = 55.466  #(degrees_north)
meta.lon = -60.2   #(degrees_east)
meta.year = 1962
meta.month = 8
meta.day = 9
meta.levels=len(depth)
meta.typ3= 'XBT'  #consistent with WOD code table: https://www.ncei.noaa.gov/access/world-ocean-database/CODES/wod-datasets.html
meta.gebcodepth=qc.get_gebcodepth(meta)

# make CODCQC v1.0 check
#### it will return two variables: myflagt and kflagt_T_checks
#myflagt: the final flag combing all checks at each observed depth. 0 denotes accpeted value, 1 denotes rejected values
#myflagt_checks:  the flag of each QC check (14 checks in total)at each observed epth. 0 denotes accpeted value, 1 denotes rejected values
[myflagt, kflagt_T_checks] = qc.check_T_main(tem, depth, meta)

#print the temperature QC result
print('Temperature QC result is:',myflagt)
print('QC result of each check is:')
for i,name in enumerate(const.QCcheck_T_name):
    print(name+' is: ',kflagt_T_checks[i])
```

#### 4.4.2 Execution of a single specific check

You can also run a single specific QC check on your own. For example:

```python
import CODCQC
from CODCQC import CODCQC_main
from CODCQC.qc_T_models import *
import numpy as np

#initialize the QC class  
qc = CODCQC_main.QualityControl()  #you need to wait for 1-2 minutes

depth = [0.0, 5.598, 7.800, 11.200, 14.000, 16.600, 20.000, 21.299]
tem = [9.1, 8.7, 8.3, 7.2, np.nan , 5.1, 4.4, 4.5]
meta=CODCQC.metaData()
meta.lat = 55.466  
meta.lon = -60.2   
meta.year = 1962
meta.month = 8
meta.day = 9
meta.levels=len(depth)
meta.typ3= 'XBT'

#For example: Run the local climatological range check and return the flag of this specific check
[temflag,_,_] = aqc_check7.climatology_check(qc, depth, tem, meta)
print(temflag)
```

## 5. References

+ #### For more information about the CODC-QC, please refer the documents or links below:

> CODCQC Github Project:  https://github.com/zqtzt/CODCQC
>
> IAP ocean and climate website: http://www.ocean.iap.ac.cn/pages/dataService/dataService.html?navAnchor=dataService
>

- #### **For more information about the CODC-QC (performance evaluation, scientific application)**, please refer Tan et al., 2022 (under review)

- #### Additionally, here is **a review of quality control for ocean observations**:

> Tan, Z., B. Zhang, X. Wu, M. Dong, L. Cheng*, 2021: Quality control for ocean observations: From present to future. *Science China Earth Sciences*, https://doi.org/10.1007/s11430-021-9846-7
>

+ #### **Please remember to cite this study if you use CODCQC for scientific purpose.**  The citation is: 

  > Tan Z., Cheng L., Gouretski V., Zhang B., Wang Y., Li F., Liu Z., Zhu J., 2023: A new automatic quality control system for ocean in-situ temperature observations and impact on ocean warming estimate. Deep Sea Research Part I, 103961, https://doi.org/10.1016/j.dsr.2022.103961 

* ### License

  CODC-QC is licensed under the [Apache-2.0 License](https://github.com/zqtzt/CODC-AutoQC/blob/main/LICENSE).

+ ### References

> 【1】 Tozer, B., D. T. Sandwell, W. H. F. Smith, C. Olson, J. R. Beale, and P. Wessel, 2019: Global bathymetry and topography at 15 arc sec: SRTM15+. *Earth and Space Science*, **6**, doi:10.1029/2019EA000658.
>
> 【2】Gouretski, V., 2018: World Ocean Circulation Experiment – Argo global hydrographic climatology. *Ocean Sci.*, **14,** 1127-1146, doi:10.5194/os-14-1127-2018.
>
> 【3】Barton, Z., and I. Gonzalez, 2016: AOML high density XBT system setup instructions and troubleshooting manual.
>
> 【4】Garcia, H. E., Boyer, T. P., Locarnini, R. A., Baranova, O. K., & Zweng, M. M. (2018). World Ocean Database 2018: User’s Manual. *Silver Spring: National Oceanic and Atmospheric Administration*.

## 6. Acknowledgment

​	The R&D of CODCQC is supported by the Strategic Priority Research Program of the Chinese Academy of Sciences [Grant no. XDB42040402], the National Natural Science Foundation of China [Grant no. 42122046, 42076202), National Key R&D Program of China [Grant no. 2017YFA0603202], Key Deployment Project of Centre for Ocean Mega-Research of Science, CAS [Grant no. COMS2019Q01] and open fund of State Key Laboratory of Satellite Ocean Environment Dynamics, Second Institute of Oceanography, MNR [Grant no. QNHX2133]. We thank the help of the IQuOD team for providing the open-source AutoQC packages and Oceanographic Data Center, CAS for support in data analysis.

## 7. Questions and feedback

​	We are warmly welcome feedback/questions/fork/pull requests/improved the CODC-QC project!!

​	If you have any questions/suggestions about this program, or if you find some bugs in this program, or even if you are willing to debug/improved the CODC-QC project, please feel free and do not hesitate to tell us via:

+ [Create an issue](https://github.com/zqtzt/CODC-AutoQC/issues) in the Github community

+ [Pull requests](https://github.com/zqtzt/CODC-AutoQC/pulls]) your debugged/improved codes in the Github community

+ Send an email to us: <font color=#0099ff><u>tanzhetao@mail.iap.ac.cn</u> </font><font color=#0099ff> or <u>chenglij@mail.iap.ac.cn</u> </font>


## 8. Update log

2021.10.13  The first version of CODCQC User Manual  (version 0.1.0) is released.

2021.12.30  Revision of CODCQC User Manual (version 0.1.1) is released.

2022.10.13  Revision of CODCQC User Manual (version 0.1.2) is released.

2023.1.18 The CODCQC (version 1.0) Python Package and the CODCQC User Manual (version 1.0) are released.





