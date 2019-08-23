#note you need to run pip install pytenable
import requests
import json
import sys

from tenable.sc import TenableSC
sc = TenableSC('10.10.89.251', port=443)
sc.login('svc-jenkins', 'R#*3AduDTNIqJ*g')
iplist=sys.argv
iplist.pop(0)
try:
    resp=sc.get('scan/2298')
    responsedict=resp.json()
    print (responsedict)
    sc.scans.edit(2298, name='VULN-Standard Scan Configurable',targets=iplist)
    running = sc.scans.launch(2298)
    print('The Scan Result ID is {}'.format(running['scanResult']['id']))    
except Exception as e:
    print(e)
    
    