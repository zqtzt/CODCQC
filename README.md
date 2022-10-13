# CODCQC

__**The user manual of CODC-QC is available now!! ((clip here)[https://github.com/zqtzt/CODCQC/]) **__


**An open source Python interface to the quality control of ocean in-situ observations.**

CODC-QC (CAS-Ocean Data Center (CODC) Quality Control system) is an open source Python interface to the quality control of ocean *in-situ* observations (e.g, temperature profiles, salinity profiles etc.). It was developed to reduce human-workload and time-consuming on manual quality control as well as adapt the increasing volume of daily real-time data flow on observing system and large data centers. 

The *in-situ* observations collected from the ocean are quality-heterogeneous. Decades of efforts have been dedicated to developing different manual or automatic quality control (QC) system to improve the quality and availability of ocean database, which is one of the basic tasks in many oceanic studies.

The goals of developing the auutomatic QC (AutoQC) is to provide a quality-hemogeonous database, with reduciing human-workload and time-consuming on manual QC as well as adapting the increasing volume of daily real-time data flow on observing system and large data centers. 

Here, we delveoped an AutoQC system (we refer to this procedure as **CODC-QC** system (CAS-Ocean Data Center Quality Control system) to quality control the ocean *in-situ* observations. 



> #### Why CODC_QC

- CODC-QC contains several QC checks that can be easily combined and tuned by users.
- CODC-QC provides many typical data interface for inputting raw data.
- The QC flags in CODC-QC are optional multiple categories, which depends on user's purposes.
- CODC-QC is a climatology-based automatic quality control algorithm. It is good at detecting bad data with paying an acceptable low price of sacrificing good data.
- The performance of CODC-QC has been meticulously analyzed and evaluated by comparing it with other international QC systems (see Tan et al., 2022; under review).

**In this version, CODC-QC is only avaliable for temperature observations**. It convers all temperature data instrument types (e.g., Bottle, XBT, CTD, Argo, APB etc.).  In the future, CODC-QC will extent to salinity observations and oxygen observations.


​	We are warmly welcome feedback/questions/fork/pull requests/improved the CODC-QC project!!

​	If you have any questions/suggestions about this program, or if you find some bugs in this program, or even if you are willing to debug/improved the COMS_QC project, please feel free and do not hesitate to tell us via:

+ [Create an issue](https://github.com/zqtzt/COMS-AutoQC/issues) in the Github community

+ [Pull requests](https://github.com/zqtzt/COMS-AutoQC/pulls]) your debugged/improved codes in the Github community

+ Send an email to us: <font color=#0099ff><u>tanzhetao@mail.iap.ac.cn</u> </font><font color=#0099ff> or <u>chenglij@mail.iap.ac.cn</u> </font>



Author: Zhetao Tan (<font color=#0099ff><u>tanzhetao@mail.iap.ac.cn</u></font>) 
Contributor: Lijing Cheng, Viktor Gourestki, Yanjun Wang, Bin Zhang
Center for Ocean Mega-Science, Chinese Academy of Sciences (COMS/CAS)
Institute of Atmospheric Physics, Chinese Academy of Sciences (IAP/CAS)


**Reference: Tan Z., Cheng L., Gouretski V., Zhang B., Wang Y., Li F., Liu Z., Zhu J., 2022: A new automatic quality control system for ocean in-situ temperature observations and impact on ocean warming estimate. Deep Sea Research Part I (under review)**



License: [Apache-2.0 License](https://github.com/zqtzt/COMSQC/blob/main/LICENSE)
