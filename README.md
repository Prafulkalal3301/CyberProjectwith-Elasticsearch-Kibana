# CyberProjectwith-Elasticsearch-Kibana

This is python project to get following details of a machine and report to Kibana dashboard.
</br>

: Machine status(UP or DOWN)
```python
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
```

: Antivirus status

: Antivirus information about Up-to-date, exe file
```python

proc = subprocess.Popen(["powershell", "powershell -executionpolicy bypass -File avcheck.ps1"],
                        stdout=subprocess.PIPE);
```           
: packages present in the machine
```python
print("\n===Programs installed in machine===")

process = subprocess.Popen(["powershell",
                            "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName | Format-List"],
                           stdout=subprocess.PIPE);
 ```                          
: hostname

: ipaddress
```python
hostname = socket.gethostname()
hoip = socket.gethostbyname(hostname)
```

# creating indexes and reporting to dashboard
Setting up database


```python

from elasticsearch import Elasticsearch
HOST_URLS=["http://127.0.0.1:9200"]
esconn=Elasticsearch(HOST_URLS)

esconn.indices.create(index='windowspc', ignore=400)
esconn.indices.create(index='windowspacks', ignore=400)
esconn.indices.create(index='hoststatus',ignore=400)
 ```
 
 
# Indexing antivirus info

```python
esconn.index(
        index="windowspc",
        doc_type="avsinfo",
        id=i,
        body={
            'name':name,
            'updatestatus':update,
            'status':status,}
    )

```

# Indexing packages info

```python
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
```

# Indexing hostname and hostip info
```python
esconn.index(index="hoststatus",
             id=0,
             body={
                 "hostname":hostname,


                 "hoststatus":hodata,
                 "ipaddress":hoip,

})

```

