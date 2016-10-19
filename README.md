# Project

CU-Z62 Q189-F11 Testing

![ATS-Front](/q189-ats-front.png)
![ATS-Back](/q189-ats-back.png)

# Test Log Files

- 2011.log: dlt645tst
- 2012.log: xdlms
- 2020.log: dlt645tst
- 2021.log: dlt645tst
- 2022.log: xdlms
- 2023.log: xdlms

# Bad DLMS APDU

FFC3 can see a very strange dlms response that contains
a corrupted DLMS apdu encapsulated in a valid HDLC frame.
This *possibly* means meter DLMS tx buffer damaged. Below
are detail log locations:

- 2023.log:1596
- 2023.log:1005499
- 2023.log:1434241

# F11 Occurences

- 8083 (E650): 2016-10-17 17:45:28 (1476697528) ![setup-1](/setup-1.png)
    - 2011.log:249725 dlt645 timeout
    - 2012.log:170592 dlms timeout, then send DM after several secs
- 8034 (E650): 2016-10-18 19:53:27 (1476791607) ![setup-1](/setup-1.png)
    - 2020.log:302470 dlt645 timeout
    - 2022.log:333327 dlms timeout, then send DM after several secs
- 0663 (E850): 2016-10-18 23:01:41 (1476802901) ![setup-2](/setup-2.png)
    - 2021.log:452403 dlt645 timeout
    - 2023.log:634572 dlms timeout, then send DM after several secs

