from flask import Flask
import sys
app = Flask(__name__)
try:
    #two parameters for script first can be any server or consul vip,  second is whether to do a dif
    address=sys.argv[1]
except:
    address='laxqanrexmt.office.cyberu.com'  # default for debugging if nothing is passed in
    #messagebox.showinfo("Title", "Nothing Passed in")    


def refreshdata():
    outdir="e:\\ConsulJenkins\\" + address +"\\"
    fnamestamp=outdir+"\\stamp"
    with open(fnamestamp) as f:
        comparestamp = f.read().strip()
    bsedi =outdir+comparestamp
    return bsedi
 
def getclientdata():
    bsedi=refreshdata()
    fnamenodes=bsedi+"\\clients"
    with open(fnamenodes) as f2:
        clients = f2.read().strip()
    return clients
def getserverdata():
    bsedi=refreshdata()
    fnameservers=bsedi+"\\servers"
    with open(fnameservers) as f1:
        servers = f1.read().strip()   
    return servers
def getexco():
    bsedi=refreshdata()
    fnameservers=bsedi+"\\exco"
    with open(fnameservers) as f1:
        exco = f1.read().strip()   
    return exco
def getexmt():
    bsedi=refreshdata()
    fnameservers=bsedi+"\\servers"
    with open(fnameservers) as f1:
        servers = f1.read().strip() 
    fnamenodes=bsedi+"\\clients"
    with open(fnamenodes) as f2:
        clients = f2.read().strip()
    computers=str(servers+" "+ clients)
    arcomputers=computers.split(" ")
    exmt=""
    space=""
    for computer in arcomputers:
        lowcomputer=str(computer).lower()
        if "exmt" in str(lowcomputer):
            exmt=exmt + space + str(computer)
            space=" "
    return exmt

        
@app.route('/<address>/clients')
def show_clients(address):
    clients=getclientdata()
    # show the user profile for that user
    return clients

@app.route("/")
def hello():
    return "ConsulInfo"

@app.route('/<address>/servers')
def show_servers(address):
    # show the user profile for that user
    servers=getserverdata()
    return servers

@app.route('/<address>/exmt')
def show_exmt(address):
    # show the user profile for that user
    exmt=getexmt()
    return exmt
@app.route('/<address>/exco')
def show_exco(address):
    # show the user profile for that user
    exco=getexco()
    return exco
if __name__ == '__main__':
    app.run(debug=True)