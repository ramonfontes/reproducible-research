### Bibtex:

@article{Campolo2018,
  doi = {10.3390/s18124435},
  url = {https://doi.org/10.3390/s18124435},
  year  = {2018},
  month = {dec},
  publisher = {{MDPI} {AG}},  
  volume = {18},
  number = {12},
  pages = {4435},
  author = {Claudia Campolo and Ramon Fontes and Antonella Molinaro and Christian Esteve Rothenberg and Antonio Iera},
  title = {Slicing on the Road: Enabling the Automotive Vertical through 5G Network Softwarization},
  journal = {Sensors}
}

## Single controller approach

**Requirements:**
* Ryu   
* FreeRadius 

#### FreeRadius (Consider the following setup)

**clients.conf**  
`client 192.168.0.201 {  
        secret=secret  
        shortname=sdn_ap  
}`

`client 192.168.0.202 {
        secret=secret
        shortname=sdn_ap
}`

`client 172.16.0.203 {
        secret=secret
        shortname=sdn_ap
}`

`client 192.168.0.204 {
        secret=secret
        shortname=sdn_ap
}`

**users**  
`bob     Cleartext-Password := "hello"`   
`joe     Cleartext-Password := "sdnteam"`


**Terminal 1**
* `sudo python single-c-approach.py` 

**Terminal 2**
* `git clone https://github.com/ramonfontes/ryu -b dev`    
* `cd ryu`   
* ~/ryu$ `PYTHONPATH=. ./bin/ryu-manager ryu/app/vanet_run.py ryu/app/simple_switch_13.py`     

**Extract dataset from data-log/sta1.log**   
**>> you have to modify [vanet_run.py](https://github.com/ramonfontes/ryu/blob/dev/ryu/app/vanet_run.py#L134) in order to run the correct case.**

## Multiple controller approach

**Requirements:**
* Ryu   
* Docker containers  
* python-scapy  

**Terminal 1**
* $ sudo docker run -it --privileged=true --name c0 --hostname=c0 --pid=host ubuntu /bin/bash   
* c0# `git clone https://github.com/ramonfontes/ryu -b book`    
* c0# `cd ryu`   
* c0# ~/ryu$ `PYTHONPATH=. ./bin/ryu-manager ryu/app/wifi.py`     

**Terminal 2**
* $ sudo docker run -it --privileged=true --name c1 --hostname=c1 --pid=host ubuntu /bin/bash   
* c1# `git clone https://github.com/ramonfontes/ryu -b book`    
* c1# `cd ryu`   
* c1# ~/ryu$ `PYTHONPATH=. ./bin/ryu-manager ryu/app/wifi.py`     

**Terminal 3**
* $ sudo docker run -it --privileged=true --name c2 --hostname=c2 --pid=host ubuntu /bin/bash   
* c2# `git clone https://github.com/ramonfontes/ryu -b book`    
* c2# `cd ryu`   
* c2# ~/ryu$ `PYTHONPATH=. ./bin/ryu-manager ryu/app/wifi.py`     

**Terminal 4**
* $ sudo python multi-c-approach.py  


**Extract dataset from ping.txt  (slicing federation is the default one)**    
**>> in order to test no-slicing federation case, a minor change in [wifi.py](https://github.com/ramonfontes/ryu/blob/book/ryu/app/wifi.py) is required (specially the [load value reference](https://github.com/ramonfontes/ryu/blob/86d130b11de5024313b122ce0875c222a6590a85/ryu/app/wifi.py#L152)).**

![](https://github.com/ramonfontes/reproducible-research/blob/master/mininet-wifi/V2X-Slicing/arq-multi-c.png)   
Figure 1. Proposed prototype for multiple controller approach


