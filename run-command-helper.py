import boto3
import os
import sys
import time

import logging as log

log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s %(message)s')

log.getLogger('boto3').setLevel(log.ERROR)
log.getLogger('botocore').setLevel(log.ERROR)
log.getLogger('s3transfer').setLevel(log.ERROR)

def run_powershell_script(instanceId, command, workingDirectory,returnstndout=0):

    client = boto3.client('ssm')
    response = client.send_command(
        InstanceIds=[instanceId],
        DocumentName="AWS-RunPowerShellScript",
        Comment="AWS-RunPowerShellScript",
        Parameters={
            'commands': [command],
            "workingDirectory" : ["C:\ExpresslaneScripts"],
            "executionTimeout": ["900"]
        },
    )

    # Fetch CommandId to poll the command status
    log.info(response)
    command_id = response['Command']['CommandId']

    # Poll/Wait until the command status is not in Pending state
    while True:
        time.sleep(2)
        output = client.get_command_invocation(
            CommandId = command_id,
            InstanceId = instanceId,
        )
        log.info(output)
        if (output['Status'] == 'Pending') or (output['Status'] == 'InProgress'):
            continue
        else:
            break
    if len(sys.argv) > 4:
        print (output['StandardOutputContent'])
        return output['StandardOutputContent']        
        
    

if __name__ == '__main__':
    run_powershell_script(sys.argv[1], sys.argv[2], sys.argv[3])
       