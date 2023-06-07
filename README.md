# Prisma SD-WAN ION Rebooting (Preview)
The purpose of this script is to rebooting an ION elemeent

If you use the name "ALL-IONS" it will reboot all IONs. 

#### License
MIT

#### Requirements
* Active CloudGenix Account - Please generate your API token and add it to cloudgenix_settings.py
* Python >=3.7

#### Installation:
 Scripts directory. 
 - **Github:** Download files to a local directory, manually run the scripts. 
 - pip install -r requirements.txt

### Examples of usage:
 Please generate your API token and add it to cloudgenix_settings.py

 1. ./reboot.py --name Branch-Site-1-ION1
      - Will reboot the ION named Branch-Site-1-ION1
 2. ./reboot.py --name ALL-IONS
      - Will reboot all IONs so be careful 

### Caveats and known issues:
 - This is a PREVIEW release, hiccups to be expected. Please file issues on Github for any problems.

#### Version
| Version | Build | Changes |
| ------- | ----- | ------- |
| **1.0.0** | **b1** | Initial Release. |


#### For more info
 * Get help and additional Prisma SD-WAN Documentation at <https://docs.paloaltonetworks.com/prisma/cloudgenix-sd-wan.html>
PrismaAccess2023