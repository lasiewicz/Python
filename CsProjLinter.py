#!/usr/bin/python 
import json, os, fnmatch, re
import xml.etree.ElementTree
import sys, glob

def main():

    ERROR_MESSAGE = MessageState()
    WARNING_MESSAGE = MessageState()

    with open('packageLinter/lintedPackages.json') as f:
        lintingPackages = json.load(f)

    serviceDirectory =  sys.argv[1]
    csprojFileList = []

    for root, dirnames, filenames in os.walk(serviceDirectory):
        for csrprojFile in fnmatch.filter(filenames, '*.csproj'):
            csprojFileList.append(os.path.join(root, csrprojFile))

    # Iterate over CsProj files
    for csProjFile in csprojFileList:
        e = xml.etree.ElementTree.parse(csProjFile).getroot()

        packageNodes = []
        ItemGroupeNodes = e.findall("ItemGroup")
        for itemGroups in ItemGroupeNodes:
            for node in itemGroups.getiterator():
                if node.tag == 'PackageReference':
                    packageNodes.append(node)

        # Iterate over Linted Packages
        for package in lintingPackages["packages"]:
            lPackage = MapLintedPackageFromFile(package)

            # Skip linting project file if it does not match regex
            if (not CheckTargetProjMatch(lPackage, csProjFile)):
                continue

            # will fail build if linted package is required
            packageFound = False 

            # Iterate over CsProj file packages
            for pNode in packageNodes:
                curPackageName    = str(pNode.get("Include"))

                # Handles edge case when version is lowercase
                if str(pNode.get("Version")) != "None":
                    curPackageVersion = str(pNode.get("Version")).split("-")[0]
                else:
                    curPackageVersion = str(pNode.get("version")).split("-")[0]

                if (lPackage.packageName == curPackageName):
                    packageFound = True

                    if lPackage.packageVersion.packageRelation != None:
                        curPackageVersionNumbers     = [int(x) for x in str.split(curPackageVersion, ".")]
                        lintedPackageVersionNumbers  = [int(x) for x in str.split(lPackage.packageVersion.packageVersionNumber, ".")]

                        # We verify the NuGet version is greater than or equal than the linted version
                        if (lPackage.packageVersion.packageRelation == "gteq"):
                            satisfiesVersionConstraint = True
                            for i in range(min(len(curPackageVersionNumbers), len(lintedPackageVersionNumbers))):
                                if curPackageVersionNumbers[i] < lintedPackageVersionNumbers[i]:
                                    satisfiesVersionConstraint = False
                                    break
                                elif curPackageVersionNumbers[i] > lintedPackageVersionNumbers[i]:
                                    break
                                # We continue iterating if numbers are equal                                

                            if (not satisfiesVersionConstraint): 
                                SetMessage("Package " + lPackage.packageName + " " + curPackageVersion + " in " +  csProjFile + " must be updated to " + lPackage.packageVersion.packageVersionNumber + " or higher. " + lPackage.buildMessage , lPackage, ERROR_MESSAGE, WARNING_MESSAGE) 

            # Fail if Required package is not found
            if (lPackage.isRequired == True and packageFound == False):
                SetMessage("Package " + lPackage.packageName + " " + lPackage.packageVersion.packageVersionNumber + " is required in " +  csProjFile + " and needs to be installed", lPackage,  ERROR_MESSAGE, WARNING_MESSAGE) 

    Exit(WARNING_MESSAGE, ERROR_MESSAGE)

def MapLintedPackageFromFile(package):
    lPackage = LintedPackage()
    lPackageVersion = PackageVersion()
    lPackage.packageVersion = lPackageVersion

    lPackage.packageName = str(package["packageName"]) or None
    lPackage.buildMessage = str(package["buildMessage"]) or None
    lPackage.isRequired = bool(package["required"]) or None
    lPackage.targetProjects = package["targetProjects"] or None
    lPackage.targetProjects = [ str(proj)  for proj in lPackage.targetProjects]
    lPackage.buildAction = str(package["buildAction"]) or None
    lPackage.packageVersion.packageVersionNumber = str(package["version"]["number"]) or None
    lPackage.packageVersion.packageRelation = str(package["version"]["relation"]) or None

    return lPackage


# Checks if the given CsProj file matches any of the given Regex Expressions
def CheckTargetProjMatch(package, csProjFile):
    CsProjFileMatches = False
    regexExpressions = [expr.strip() for expr in  package.targetProjects]

    for curRegEx in regexExpressions:
        csProjRegEx = re.compile(curRegEx)
        if (csProjRegEx.search(csProjFile)):
           CsProjFileMatches = True 

    return CsProjFileMatches

def SetMessage(message, lintedPackage, ERROR_MESSAGE, WARNING_MESSAGE):
    if lintedPackage.buildAction == "fail":
        ERROR_MESSAGE.message +=  "\n " + message
    elif lintedPackage.buildAction == "warn":
        WARNING_MESSAGE.message +=  "\n " + message
    return

def Exit(WARNING_MESSAGE, ERROR_MESSAGE):

    if WARNING_MESSAGE.message != "":
        print(WARNING_MESSAGE.message)
    if ERROR_MESSAGE.message != "":
        print(ERROR_MESSAGE.message)
        sys.exit(1)
    else:
        sys.exit(0)

class LintedPackage:
    def __init__(self, packageName = None, packageVersion = None, isRequired = None, targetProjects = None, buildAction = None, buildMessage = None):
        self.packageName = packageName 
        self.packageVersion = packageVersion 
        self.isRequired = isRequired 
        self.buildMessage = buildMessage
        self.targetProjects = targetProjects
        self.buildAction = buildAction 

class PackageVersion:
    def __init__(self, packageVersionNumber = None, packageRelation = None):
        self.packageVersionNumber = packageVersionNumber
        self.packageRelation = packageRelation

class MessageState:
    def __init__(self, message = ""):
        self.message =message 


if __name__ == "__main__":
    main()
