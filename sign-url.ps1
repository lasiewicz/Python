param (
        [string]$EnvironmentType,[string]$Environment
 )


$signpath="s3://sandbox-inf-ls-dev-us-west-2-el-deploymentlogs/" + $Environment +"status.html"
$site=aws s3 presign $signpath --expires-in 604800
Write-Host($site)