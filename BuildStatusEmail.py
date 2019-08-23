import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

import pyodbc
import datetime
import time

def sendEmail():
    	fromaddr = "builds@csod.com"
        toaddr = "DLReleaseManagementGroup@csod.com"
    
    	msg = MIMEMultipart()

	HTMLmsg = """\
	<html>
	<body>
	<style>
	table {
    		font-family: arial, sans-serif;
    		border-collapse: collapse;
   		width: 100%;
	}

	td, th {
    		border: 1px solid black;
    		text-align: center;
		line-height: 1.6;
    		padding: 10px;
		font-size:x-small;
		}
	</style>

	<h3>Build Summary Report - """ + time.strftime("%b %d, %Y") + """</h3>
	<table>
	<tr>
	<td><strong>QA Environment</strong></td>
	<td><strong>Branch</strong></td>
	<td><strong>Build Status</strong></td>
	<td><strong>Start Time</strong></td>
	<td><strong>End Time</strong></td>
	<td><strong>Total Time</strong></td>
	<td><strong>Warning / Failure Summary</strong></td>
	</tr>
	"""
	successCount = 0
	for QAenv in (1,2,3,4,5,7):
		if(checkBuildEnd(QAenv) == "SUCCESS"):
			statusColor = "green"
			successCount = successCount + 1
		else:
			statusColor = "red"

		if(getNumFailures(QAenv) > 0):
			buffer = getFailedSteps(QAenv)
			textColor = "red"
			align = "left"
		else:
			buffer = "No warning / failures"
			textColor = "green"
			align = "center"

		HTMLmsg = HTMLmsg + """<tr> \
			<td><strong>QA0""" + str(QAenv) + """</strong></td> \
			<td><a href="file://lax-qa-build0""" + str(QAenv) +"""/e$/TFS/Build/QA0""" + str(QAenv) +""" ">""" +str(getQAName(QAenv)) + """</a></td> \
			<td><strong style="color: """+ statusColor +""" ">""" + str(checkBuildEnd(QAenv)) + """</strong></td> \
			<td>""" + getStartTime(QAenv).time().strftime("%H:%M:%S") + """</td> \
			<td>""" + getEndTime(QAenv).time().strftime("%H:%M:%S") + """</td> \
			<td>""" + str(round((getEndTime(QAenv) - getStartTime(QAenv)).total_seconds()/3600,2)) + """</td> \
			<td style="text-align: """+ align +"""; color: """+ textColor +""" ">""" + buffer + """</td> \
			</tr>"""
	HTMLmsg = HTMLmsg + """
			</table>
			<p> More detailed Build Status information can be found at http://ci-master/BuildStatus/ </p>
			</body> \
			</html>"""

    	msg['From'] = fromaddr
    	msg['To'] = toaddr
	if successCount == 6:
    		msg['Subject'] = "Build Report - " + time.strftime("%b %d, %Y") + " (PASS)"
	else:
		msg['Subject'] = "Build Report - " + time.strftime("%b %d, %Y") + " (FAIL)"

	msg.attach(MIMEText(HTMLmsg, 'html'))

    	server = smtplib.SMTP('10.7.8.157')
    	text = msg.as_string()
    	server.sendmail(fromaddr, toaddr, text)
    	server.quit()

def connectDB(query):
    	server = 'CI-MASTER\SQL2014,64221'
    	database = 'ConfigurationService'
    	username = 'OFFICE\Builduser'
    	password = 'buildM3!'
    	cnxn = pyodbc.connect('Trusted_Connection='+"Yes"+';DRIVER={ODBC Driver 11 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    	cursor = cnxn.cursor()
    	result = cursor.execute(query)

    	return result

def checkBuildEnd(QAenv):
    	query = "SELECT COUNT(*) FROM [BuildStatus].[dbo].[ActivityLog] WHERE Operation = 'BUILD END' AND OperationStatus_ID = 1 AND BuildDefinition_ID =" + str(QAenv)
    	result = connectDB(query).fetchone()[0]
    	if result == 1:
        	return "SUCCESS"
    	else:
        	return "INCOMPLETE / FAILURE"

def getQAName(QAenv):
    	query = "SELECT BuildDescription FROM [BuildStatus].[dbo].[BuildDefinition] WHERE ID =" + str(QAenv)
    	result = connectDB(query).fetchone()[0]
    	return result

def getNumFailures(QAenv):
    	query = "SELECT COUNT(*) FROM [BuildStatus].[dbo].[ActivityLog] WHERE OperationStatus_ID != 1 AND BuildDefinition_ID =" + str(QAenv)
    	result = connectDB(query).fetchone()[0]
	return result

def getFailedSteps(QAenv):
	query = "SELECT Operation FROM [BuildStatus].[dbo].[ActivityLog] WHERE OperationStatus_ID != 1 AND BuildDefinition_ID =" + str(QAenv)
    	result = connectDB(query)
	ctr = 1
	buffer = ""
	if result != "":
    		for row in result:
        		buffer += str(ctr) + ") " +str(row[0]) + "<br />"
			ctr = ctr+1
	return buffer
		

def getBuildDetails(QAenv):
    	buffer = "Build Summary for QA0"+ str(QAenv) + "/" + getQAName(QAenv) + "\n"
    	query = "SELECT [Timestamp] FROM [BuildStatus].[dbo].[ActivityLog] WHERE Operation = 'BUILD START' AND BuildDefinition_ID =" + str(QAenv)
    	startTime = connectDB(query).fetchone()[0]
    	buffer += "	Start time = " + str(startTime.time()) + "\n"
    	query = "SELECT [Timestamp] FROM [BuildStatus].[dbo].[ActivityLog] WHERE Operation = 'BUILD END' AND BuildDefinition_ID =" + str(QAenv)
    	endTime = connectDB(query).fetchone()[0]
    	buffer += "	End time = " + str(endTime.time()) + "\n"
    	buffer += "\nBuild Status = SUCCESS\n\n"
    	return buffer

   
def getStartTime(QAenv):
    	query = "SELECT [Timestamp] FROM [BuildStatus].[dbo].[ActivityLog] WHERE Operation = 'BUILD START' AND BuildDefinition_ID =" + str(QAenv)
    	startTime = connectDB(query).fetchone()[0]
	return startTime


def getEndTime(QAenv):
	query = "SELECT [Timestamp] FROM [BuildStatus].[dbo].[ActivityLog] WHERE Operation = 'BUILD END' AND BuildDefinition_ID =" + str(QAenv)
	if checkBuildEnd(QAenv) == "SUCCESS":
    		endTime = connectDB(query).fetchone()[0]
	else:
		endTime = datetime.datetime.now()
	return endTime


def main():
    	sendEmail()
    	print("FIN.")


if __name__ == "__main__":
    	main()