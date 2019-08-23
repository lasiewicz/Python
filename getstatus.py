import os, fnmatch,io
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result
configlist=[]
lstdir=['E:\project\\exen\\Apps','E:\\project\\exen\\CSODApps','E:\\project\\exmh','E:\\project\\exmh\\CSODApps','E:\\project\\exmt1\\CSODApps','E:\\project\\exmw','E:\\project\\ssrs','E:\\project\\exmt1\\apps']

for d in lstdir:
    findi=find('*.exe.config', d)
    if findi:
        for x in findi:
            cdir=str(x)
            if not 'roslyn' in cdir:
                configlist.append(cdir)  

                
    for i,j,y in os.walk(d):
        curdir=str(i)
        if "rest-mq-service" in curdir:
            print ("stop")        
        if not 'roslyn' in curdir:
            webconfig= curdir+'\\web.config'
            appjson= curdir+'\\appsettings.json'
            configjson=curdir+'\\configjson'
            if os.path.exists(webconfig):
                configlist.append(webconfig)
            if os.path.exists(appjson):
                configlist.append(appjson) 
            if os.path.exists(configjson):
                configlist.append(configjson)             

with open('listfile2.txt', 'w') as filehandle:
    for listitem in configlist:
        filehandle.write('%s\n' % listitem)
        
            

