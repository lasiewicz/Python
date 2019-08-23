import __builtin__
deploylist = [{'BuildNumber': '39', 'ComponentName': 'comp-salaryrange-api'}, {'BuildNumber': '197', 'ComponentName': 'search-query-service'}]
apple="comp-salaryrange-api"

y=False
if apple in str(deploylist):
    y = True

print y


