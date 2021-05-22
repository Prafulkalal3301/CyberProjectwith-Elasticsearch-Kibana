import os
import re


from elasticsearch import Elasticsearch
HOST_URLS=["http://127.0.0.1:9200"]
esconn=Elasticsearch(HOST_URLS)
import hashlib
esconn.indices.create(index='windowspc', ignore=400)
esconn.indices.create(index='windowspacks', ignore=400)
esconn.indices.create(index='hoststatus',ignore=400)
import socket
import re
import subprocess
from django.shortcuts import render
from django.http import HttpResponse
from subprocess import Popen, PIPE
avs=[]
SOMEHOST = "google.com"
Trace = os.system("tracert " + SOMEHOST + "> pin_out.txt")
TTl = os.system("ping " + SOMEHOST + " >ttl.txt")

HOST_UP = True if os.system("ping " + SOMEHOST) is 0 else False
A1 = HOST_UP
if HOST_UP == True:
    hodata="UP"
    chops = open("pin_out.txt", "r")
    cttl = open("ttl.txt", "r")

    lines = cttl.readlines()[2:3]

    s = re.findall(r'\S+', lines[0])
    bttl = s[-1]
    ttl = bttl.lstrip('TTL=')
    print(ttl)
    li = []
    hoplines = chops.readlines()[3:-1]
    for i in hoplines:
        if i != "\n":
            li.append(i)
    hops = len(li)
    A = int(ttl) + hops
    print(A)
    print("Check the os (ttl+hops) of machine: ", A)
else:
    hodata="DOWN"
    print("Host is unreachable ")

print("IS HOST UP: ", HOST_UP)
print("\n")

#os.system('WMIC /Node:localhost /Namespace:\\root\SecurityCenter2 Path AntiVirusProduct Get displayName /Format:List')


print("===Antivirus status===\n")
# B1 = os.system('powershell -executionpolicy bypass -File .\avcheck.ps1 | Out-File -FilePath A:\CybrProj\avv.txt')

proc = subprocess.Popen(["powershell", "powershell -executionpolicy bypass -File avcheck.ps1"],
                        stdout=subprocess.PIPE);
res = proc.communicate()[0]
lie = res.decode()

av=open('av.txt','w')
av.write(lie)
av=open('av.txt','r')
line=av.readlines()
for i in line:
    if i!="\n":
        avs.append(i)






def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1

for i in range(2,len(avs)):
    pickk=avs[i]
    pick=listToString(avs[i])

    lo=list(filter(None, pick.split('  ')))
    update=lo[0]
    name=lo[1]
    if lo[2]=='\n':
        status="unknown"
    else:
        status=listToString(lo[2])




    esconn.index(
        index="windowspc",
        doc_type="avsinfo",
        id=i,
        body={
            'name':name,
            'updatestatus':update,
            'status':status,}
    )







# os.system('powershell.exe Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table –AutoSize')
print("\n===Programs installed in machine===")

process = subprocess.Popen(["powershell",
                            "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName | Format-List"],
                           stdout=subprocess.PIPE);
result = process.communicate()[0]
line = result.decode()
data = str(line)
f = open('file.txt', 'w')
f.write(data)
f.close()

packages = []
f = open('file.txt', 'r')
s = f.readlines()

for a in s:
    if len(a) > 15:
        packages.append(a)

hostname = socket.gethostname()
hoip = socket.gethostbyname(hostname)


esconn.index(index="hoststatus",
             id=0,
             body={
                 "hostname":hostname,


                 "hoststatus":hodata,
                 "ipaddress":hoip,

})


hostdata={"Status":{A1}}

j=len(packages)
for i in range(0,j):
    pk=packages[i].replace('DisplayName : ','')
    esconn.index(
        index="windowspacks",
        doc_type="packages",
        id=i,
        body={
            'packagesfound':packages[i]
        }
    )

print(hostname,hodata,hoip)

print("Done")




def show(request):
    return render(request, 'index.html', {'hoststatus': A1, 'pack': packages,'Av':avs,'hname':hostname,'hoip':hoip})
