import consul
import logging
import sys
import json
import os
import logging
import boto3
from botocore.exceptions import ClientError
import os.path


# Set up logging
logging.basicConfig(level=logging.DEBUG,format='%(levelname)s: %(asctime)s: %(message)s')
ParmsInput=sys.argv
ParmsInput.pop(0)
EnvironmentType=ParmsInput[0]
Environment=ParmsInput[1]
SsmClient = boto3.client('ssm')
BucketNameS3 = 'sandbox-inf-ls-dev-us-west-2-el-deploymentlogs'
s3 = boto3.client('s3')
SubDir='/spin-up-expresslane/automation/scripts'

def GetParmsFromParmStore(Environment, EnvironmentType, ssm):
    ConsulEnvirUrl = '/' + EnvironmentType + '/' + Environment + '/consul/uri'
    AdminLoginParm = '/' + EnvironmentType + '/' + Environment + '/expresslane/svc-account-username'
    AdminPasswordParm = '/' + EnvironmentType + '/' + Environment + '/expresslane/svc-account-password'
    print(ConsulEnvirUrl)
    SsmAddress= ssm.get_parameter(Name=ConsulEnvirUrl) ['Parameter']['Value']
    print(SsmAddress)
    AdminUserName =""
    ADPassword=""  
    try:
        AdminUserName =ssm.get_parameter(Name=AdminLoginParm) ['Parameter']['Value']
        ADPassword=ssm.get_parameter(Name=AdminPasswordParm) ['Parameter']['Value']      
    except Exception as Error:
        print(Error)
    return SsmAddress, AdminUserName, ADPassword
def addssmparm(object_name):
    try:
        UrlLoginParm = '/' + EnvironmentType + '/' + Environment + '/expresslane/url/log'
        Result= SsmClient.put_parameter(Name=UrlLoginParm,value=object_name) 
    except ClientError as Error:
        print(Error)
        print(Result)  
def SignAndUpload():
    # Set these values before running the program
    
    expiration = 60*100000000     
    #bucket_name = 'sandbox-inf-ls-dev-us-west-2-el-deploymentlogs'
    
    ObjectName = 'OBJECT_NAME'    
    Key = HtmlWriteFilePath
    HtmlName=Environment + "status"
    ObjectName = HtmlName+'.html'        
    print("uploading file to s3")
    print (Key)
    print(BucketNameS3)
    print(ObjectName)
    try:
        S3Response = s3.upload_file(Key,BucketNameS3,ObjectName)
    except ClientError as e:
        print(e)
        print(S3Response)

      # Generate a presigned URL to share an S3 object
    S3SignedUrl = CreatePresignedUrl(BucketNameS3, ObjectName, expiration)
    # Generate a presigned URL to list all buckets
    print("singed url")
    print (S3SignedUrl)
   
    addssmparm(ObjectName) 
       



def CreatePresignedUrl(bucket_name, object_name, expiration=604800):
    """Generate a presigned URL to share an S3 object

    Sharing an S3 object is the intended use of S3 presigned URLs. The AWS
    Python SDK also supports generating a presigned URL to perform other S3
    operations.

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        S3Response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as Error:
        logging.error(Error)
        return None

    # The response contains the presigned URL
    return S3Response    
def iniitializecounts():
    ConsulNotEnabledTotal=""   
    ResultsDict = {}
    WindowsServiceTotal=0
    NonConsulWebAppsTotal=0
    ConsulEnabledAppsTotal=0
    NonConsulAppsTotalPassed=0
    ConsulAppsPassedTotal=0
    WindowsServicePassedTotal=0
    PassingTotalReturnString=""
    FailingReturnString=""
    return ResultsDict, WindowsServiceTotal, NonConsulWebAppsTotal, ConsulEnabledAppsTotal, NonConsulAppsTotalPassed, ConsulAppsPassedTotal, WindowsServicePassedTotal, PassingTotalReturnString, FailingReturnString


    
def Writeouthtml(CumTotalAllApps, HtmlStringFileData, TotalPassingApps, TotalFailingApps, WindowsServiceTotal, WindowsServicePassedTotal, ConsulEnabledAppsTotal, ConsulAppsPassedTotal, NonConsulAppsTotal, NonConsulWebAppsPassed, FailingApps, PassingApps,ServicesRunningTextData):
    HtmlStringFileData = HtmlStringFileData.replace('cumtotal', str(CumTotalAllApps))
    replst=EnvironmentType + " " + Environment
    HtmlStringFileData = HtmlStringFileData.replace('QA-0716', replst)
    HtmlStringFileData = HtmlStringFileData.replace('cmtpassing', str(TotalPassingApps))
    HtmlStringFileData = HtmlStringFileData.replace('cmttotalfailing', str(TotalFailingApps))
    HtmlStringFileData = HtmlStringFileData.replace('WindowsServicetotal', str(WindowsServiceTotal))
    HtmlStringFileData = HtmlStringFileData.replace('WindowsServicepassing', str(WindowsServicePassedTotal))
    windowsservicefailing=WindowsServiceTotal-WindowsServicePassedTotal
    HtmlStringFileData = HtmlStringFileData.replace('WindowsServicefailing', str(windowsservicefailing))
    HtmlStringFileData = HtmlStringFileData.replace('Consultotal', str(ConsulEnabledAppsTotal))
    HtmlStringFileData = HtmlStringFileData.replace('Consulpassing', str(ConsulAppsPassedTotal))
    consulfailing=ConsulEnabledAppsTotal-ConsulAppsPassedTotal
    HtmlStringFileData = HtmlStringFileData.replace('Consulfailing', str(consulfailing))
    HtmlStringFileData = HtmlStringFileData.replace('Nontotal', str(NonConsulAppsTotal))
    HtmlStringFileData = HtmlStringFileData.replace('Nonpassing', str(NonConsulWebAppsPassed))
    nonconsulfailing=NonConsulAppsTotal-NonConsulWebAppsPassed
    HtmlStringFileData = HtmlStringFileData.replace('Nonfailing', str(nonconsulfailing))
    HtmlStringFileData = HtmlStringFileData.replace('fail!', str(FailingApps))
    HtmlStringFileData = HtmlStringFileData.replace('pass!', str(PassingApps))
    return HtmlStringFileData
def Getconsulinfo(ExpresslaneServicesDict, ParentDirectory, WindowsServiceTotal, ResultsDict, TotalPassingApps,  WindowsServicePassedTotal, TotalFailingApps, ClientDict, ConsulAppsPassedTotal, AppsPassedConsul, NonConsulWebAppsPassed, NonConsulAppsTotal,ServicesRunningData):
    TargetNonRegistered=ParentDirectory + SubDir + '/status/notregistered.txt'
    TargetNonRegistered='/home/jenkins_agent/jenkins/workspace/AWS-INFRA/INF-LS/inf-ls-expresslane/develop/validate-expresslane/automation/scripts/status/notregistered.txt'
    with open(TargetNonRegistered, "r") as text_file:
        ConsulNotEnabledTextData=text_file.read()    
    for service in ExpresslaneServicesDict:
        ConsulHealth="Not Registered in consul"
        Artifactname= str(service["Artifactname"])
        IISApplicationName = service["IISApplicationName"]
        DeployedTo = service["Domain"]
        AppType = service["AppType"]
        if AppType=='bgdtask':
            WindowsServiceTotal=WindowsServiceTotal+1
            ResultsDict[(Artifactname,'type')]='WindowsService'
            WindowsServiceName=service["WindowsServiceName"]
            ShortServiceName=WindowsServiceName
            if len(WindowsServiceName)>30:
                ShortServiceName=WindowsServiceName[:30]
            else:
                ShortServiceName=WindowsServiceName
            if ShortServiceName in ServicesRunningData:
                ConsulHealth="Windows Service running"
                ResultsDict[(Artifactname,'pass')]='1'
                TotalPassingApps=TotalPassingApps+'<tr><td><center>' + Artifactname + '</center></td><td><center>' + "Passing" + '</center></td> ' + '<td><center>' + DeployedTo + '</center></td> ' +  '<td><center>' + AppType  + '</center></td></tr> ' +  "\r\n"
                WindowsServicePassedTotal= WindowsServicePassedTotal+1
            else:
                ConsulHealth="Windows Service Not Running"
                ResultsDict[(Artifactname,'pass')]='0'
                TotalFailingApps=TotalFailingApps+'<tr><td><center>' + Artifactname + '</center></td><td><center>' + "Failing" + '</center></td> ' + '<td><center>' + DeployedTo + '</center></td> ' +  '<td><center>' + AppType  + '</center></td></tr> ' +  "\r\n"
        else: 
            if IISApplicationName in ClientDict:
                ConsulAppsPassedTotal=ConsulAppsPassedTotal+1
                ConsulHealth=ClientDict[IISApplicationName]
                AppType="Consul Enabled"
                ResultsDict[(Artifactname,'type')]='Consul'
                if ConsulHealth=='passing':
                    ResultsDict[(Artifactname,'pass')]='1'
                    TotalPassingApps=TotalPassingApps+'<tr><td><center>' + Artifactname + '</center></td><td><center>' + "Passing" + '</center></td> ' + '<td><center>' + DeployedTo + '</center></td> ' +  '<td><center>' + AppType  + '</center></td></tr> ' +  "\r\n"
                    AppsPassedConsul=AppsPassedConsul+1
                else:
                    ResultsDict[(Artifactname,'pass')]='0'  
                    TotalFailingApps=TotalFailingApps+'<tr><td><center>' + Artifactname + '</center></td><td><center>' + "Failing" + '</center></td> ' + '<td><center>' + DeployedTo + '</center></td> ' +  '<td><center>' + AppType  + '</center></td></tr> ' +  "\r\n"
            else:
                ResultsDict[(Artifactname,'type')]='NonConsul'
                ResultsDict[(Artifactname,'pass')]='1'
                try:
                    if Artifactname in ConsulNotEnabledTextData:
                        ConsulHealth="Web App"
                        NonConsulWebAppsPassed=NonConsulWebAppsPassed+1
                        NonConsulAppsTotal=NonConsulAppsTotal+1
                        TotalPassingApps=TotalPassingApps+'<tr><td><center>' + Artifactname + '</center></td><td><center>' + "Passing" + '</center></td> ' + '<td><center>' + DeployedTo + '</center></td> ' +  '<td><center>' + AppType  + '</center></td></tr> ' +  "\r\n"
                    else:
                        AppType="Consul Enabled"
                        ResultsDict[(Artifactname,'type')]='Consul'
                        ConsulAppsPassedTotal=ConsulAppsPassedTotal+1
                        ResultsDict[(Artifactname,'pass')]='0' 
                        TotalFailingApps=TotalFailingApps+'<tr><td><center>' + Artifactname + '</center></td><td><center>' + "Failing" + '</center></td> ' + '<td><center>' + DeployedTo + '</center></td> ' +  '<td><center>' + AppType  + '</center></td></tr> ' +  "\r\n"                    
                except Exception as Error:
                    print(Error)                
            print(Artifactname, " " , IISApplicationName, " " , AppType, " " , ConsulHealth)  
    return WindowsServiceTotal, TotalPassingApps,  WindowsServicePassedTotal, TotalFailingApps, ConsulAppsPassedTotal, AppsPassedConsul, NonConsulWebAppsPassed, NonConsulAppsTotal
def DownloadItemsFromS3(services_status_name):
    try:
        response = s3.download_file(BucketNameS3,'apps.html',services_status_name)
    except ClientError as Error:
        print(Error)
        print(response)
        
def readinapps(subdir, ScriptParentDirectory, target_file_name):
    json_data=ScriptParentDirectory + subdir + '/apps.json'


    with open(json_data, 'rb') as source_file:
        with open(target_file_name, 'w+b') as dest_file:
            contents = source_file.read()
            dest_file.write(contents.decode('utf-16').encode('utf-8')) 
    return ScriptParentDirectory       

def IterateConsulServices():
    """Iterates through all the tuples containing list of dictionarys returned from consul apis
    The status of each consul service is also received and this information is put into a dictionary used later
    
    """    

    for p in DictFromConsulServer:
        PrintDataOnceBool = False
        try:
            ConsulTupleServiceDetail = ConsulObject.health.service(p)
            for ConsulServiceDetail in ConsulTupleServiceDetail:
                ConsulServiceDetailInfo = ConsulServiceDetail
                for ConsulHealthDetailsDict in ConsulServiceDetailInfo:
                    if (type(ConsulHealthDetailsDict) == dict):
                        ConsulHealthInfo = ConsulHealthDetailsDict["Node"]
                        ConsulNodeName = ConsulHealthInfo["Node"]
                        status = ConsulHealthDetailsDict["Checks"]
                        for n in status:
                            healthstatus = n
                        ConsulHealthStatus = healthstatus["Status"]
                        if (PrintDataOnceBool == False):
                            ClientConsulDict[p] = ConsulHealthStatus                            
                            PrintDataOnceBool = True

        except Exception as e:
            print(e)
ScriptParentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
AppsJsonFilePathServiceStatusFilePath=ScriptParentDirectory + "/appscoverted.json"
ServiceStatusTextFilePath=ScriptParentDirectory + '/apps.html'
DownloadItemsFromS3(ServiceStatusTextFilePath)
ServicesRunningtextData = "none"
try: 
    print (ServiceStatusTextFilePath)
    print("reading in services")
    with open(ServiceStatusTextFilePath, newline='', encoding="utf16") as file:
        ServicesRunningtextData = file.read()
        print(ServicesRunningtextData)
except Exception as Error:
    print("could not read in service running")
    print(Error) 
ConsulAddress, AdminUserName, ADPassword = GetParmsFromParmStore(Environment, EnvironmentType, SsmClient)
Elservicesdict = {}
# connect to server and see what is there
ConsulObject = consul.Consul(host=ConsulAddress)
try:
    ConsulObject.connect
    TupleConsulReturn = ConsulObject.catalog.nodes()
except Exception as Error:
    print(Error)

# get leader information
try:
    ConsulReturnData = ConsulObject.status.leader()
    ConsulLeaderInfo = ConsulReturnData.rsplit(":")[0]
except Exception as Error:
    print("unable to get the leader")
    print(Error)
ConsulInfoDict = []
for Node in TupleConsulReturn:
    ConsulInfoDict = Node
ClientConsulDict = {}
ConsulTupleData = ConsulObject.catalog.services()
for ConsulServer in ConsulTupleData:
    DictFromConsulServer = ConsulServer
ScriptParentDirectory = readinapps(SubDir, ScriptParentDirectory, AppsJsonFilePathServiceStatusFilePath)
IterateConsulServices()


print(AppsJsonFilePathServiceStatusFilePath)
HtmlWriteFilePath=ScriptParentDirectory + '/statusout.html'
with open(AppsJsonFilePathServiceStatusFilePath, "r") as f:
    Elservicesdict = json.loads(f.read())
Results_dict, WindowsServiceTotal, ConsulEnabledAppsTotal, ConsulEnabledCumAppsTotal, TotalPassedConsulApps, TotalPassedConsul, TotalPassedWindowsService, PassingAppsTotal, FailingAppsTotal = iniitializecounts()
WindowsServiceTotal, PassingAppsTotal, TotalPassedWindowsService, FailingAppsTotal, ConsulEnabledCumAppsTotal, TotalPassedConsul, TotalPassedConsulApps, ConsulEnabledAppsTotal = Getconsulinfo(Elservicesdict, ScriptParentDirectory, WindowsServiceTotal, Results_dict, PassingAppsTotal, TotalPassedWindowsService, FailingAppsTotal, ClientConsulDict, ConsulEnabledCumAppsTotal, TotalPassedConsul, TotalPassedConsulApps, ConsulEnabledAppsTotal,ServicesRunningtextData)
StatusHtmlBaseFileName='/home/jenkins_agent/jenkins/workspace/AWS-INFRA/INF-LS/inf-ls-expresslane/develop/validate-expresslane/automation/scripts/status/status.html'

with open(StatusHtmlBaseFileName, 'r') as file :
    filedata = file.read()
# Replace the target string
CumTotalAppsTotal=WindowsServiceTotal+ConsulEnabledAppsTotal+ConsulEnabledCumAppsTotal
TotalPassingApss=TotalPassedConsulApps+TotalPassedWindowsService+TotalPassedConsul
TotalFailingApps=CumTotalAppsTotal-TotalPassingApss
filedata = Writeouthtml(CumTotalAppsTotal, filedata, TotalPassingApss, TotalFailingApps, WindowsServiceTotal, TotalPassedWindowsService, ConsulEnabledCumAppsTotal, TotalPassedConsul, ConsulEnabledAppsTotal, TotalPassedConsulApps, FailingAppsTotal, PassingAppsTotal,ServicesRunningtextData)
# Write the file out again
with open(HtmlWriteFilePath, 'w') as file:
    print("writing out html file")
    file.write(filedata)
try:
    SignAndUpload()
except Exception as Error:
    print(Error)
    print("error uploading to s3")
    print("file continues")
    print(filedata) 