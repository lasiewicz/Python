import xlrd 
import xlsxwriter
import os, fnmatch,io
include = xlsxwriter.Workbook("include.xlsx")
remove= xlsxwriter.Workbook("remove.xlsx")
includeworksheet = include.add_worksheet() 
excludeworksheet = remove.add_worksheet() 
includeindex=0
removeindex=0
def path_leaf(path):
    sval = path.split("\\")
    rtvalue=""
    for n in sval:
        rtvalue=n
    return rtvalue
loc = ("Keys.xlsx") 
configvalues_array = []
with open('listfile.txt') as my_file:
    for line in my_file:
        configvalues_array.append(line)
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
  
for i in range(sheet.nrows): 
    value=str((sheet.cell_value(i, 3)))
    component=str((sheet.cell_value(i, 0)))
    cfilename=str((sheet.cell_value(i, 2)))
    json=False
    #if "\'" in value:
    b=value[0]
    #print(b)
    if value[0]=="$":
        #quoteinside=value
        sval=value.split(".")
        rtvalue=""
        for n in sval:
            rtvalue=n
        quoteinside=rtvalue
        json=True
    else:
        if "='" in value:
            newvalue=value.split("=")
            configvalue=newvalue[1]
            quoteparse=configvalue.split("\'" )
            quoteinside=quoteparse[1]       
        else:
            if "\'" in value:
                configvalue=value
                quoteparse=configvalue.split("\'" )
                quoteinside=quoteparse[1]   
            else:
                if "@" in value:
                    configvalue=value
                    quoteparse=configvalue.split("@")
                    nparse=quoteparse[1]
                    if ":" in nparse:
                        tempparse=nparse.split(":")
                        quoteinside=tempparse[0] 
                        tempi=""
                    else:
                        quoteinside=nparse
                        tempi=""
                    
        #print (value)
        #print(quoteinside)
    exclude=True
    if "couchbase" in quoteinside.lower():
        exclude=True
    else:
        if component=="[COMMON CONFIG]":
            readfile=False
            exclude=False
        else:
            lastfile="!@NoneXX"
            for c1 in configvalues_array:
                line = c1.strip('\n')
                fname=path_leaf(line)
                fname=fname.lower()
                readfile=True
                testfile=cfilename
                if len(cfilename)<3:
                    testfile=fname
                    
                if not testfile.lower()==fname:
                    readfile=False
                else:
                    if "chr" in component:
                        if not "chr" in line:
                            readfile=False
                    elif "edgeimport" in component:
                        if not "edgeimport" in line:
                            readfile=False
                    else:
                        if not component in line:
                            readfile=False
                        else:
                            lastfile=line                   

                                                              
                if json==True:
                    if ".json" not in fname:
                        readfile=False
                if readfile==True:
                    lastfile=line
                    with open(line, 'r') as file:
                        data = file.read().replace('\n', '')    
                    if quoteinside in data:
                            exclude=False         
        
                   
 
    if exclude==True:
        removeindex=removeindex+1       
        c1="A" + str(removeindex) 
        c2="B" + str(removeindex)  
        c3="C" + str(removeindex)  
        c4="D" + str(removeindex)        
        excludeworksheet.write(c1, component) 
        excludeworksheet.write(c2, cfilename) 
        excludeworksheet.write(c3, value) 
        excludeworksheet.write(c4, quoteinside) 
    else:
        includeindex=includeindex+1       
        c1="A" + str(includeindex) 
        c2="B" + str(includeindex)  
        c3="C" + str(includeindex)  
        c4="D" + str(includeindex)              
        includeworksheet.write(c1, component) 
        includeworksheet.write(c2, cfilename) 
        includeworksheet.write(c3, value) 
        includeworksheet.write(c4, quoteinside)        
        
      
include.close()
remove.close()
                
                      



