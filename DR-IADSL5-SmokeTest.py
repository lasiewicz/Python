import requests
#import json
url = "http://qa-automation:5001/api/v1/trigger-tests-for-batch/11"
payload = "{\r\n  \"testBatchId\":4337,\r\n  \"RequestedBy\": \"office\\\\adavid\"\r\n}"

headers = {'Content-Type': 'application/json'}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
#responseJson = json.loads(response.text)
#print (responseJson)