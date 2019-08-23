sc.scans.copy(2298, name='VULN-Standard Scan','BLasiewicz')
#sc.scans.edit(1, name='VULN-Standard Scan')
running = sc.scans.launch(1)
print('The Scan Result ID is {}'.format(running['scanResult']['id']))
#alert = sc.alerts.detail(1)
#pprint(alert)     

