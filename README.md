# Prisma SD-WAN ION Rebooting (Preview - use at own risk)
The purpose of this script is to reboot an ION elemeent

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
 2. ./reboot.py --name -H 10
      - Will reboot device in 10 hours

### Caveats and known issues:
 - This is a PREVIEW release, hiccups to be expected. Please file issues on Github for any problems.

#### Version
| Version | Build | Changes |
| ------- | ----- | ------- |
| **1.0.0** | **b1** | Initial Release. |


#### For more info
 * Get help and additional Prisma SD-WAN Documentation at <https://docs.paloaltonetworks.com/prisma/cloudgenix-sd-wan.html>
