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
* python-scapy  

**Terminal 1**
* ~$ `cd reproducible-research/mininet-wifi/V2X-Slicing`
* ~/reproducible-research/mininet-wifi/V2X-Slicing$ `git clone https://github.com/ramonfontes/ryu -b book` 
* ~/reproducible-research/mininet-wifi/V2X-Slicing$ `cp run.sh ryu`    
* ~/reproducible-research/mininet-wifi/V2X-Slicing$ `sudo python multi-c-approach.py`             

**Extract dataset from ping.txt  (slicing federation is the default one)**    
**>> in order to test no-slicing federation case, a minor change in [wifi.py](https://github.com/ramonfontes/ryu/blob/book/ryu/app/wifi.py) is required (specially the [slicing variable](https://github.com/ramonfontes/ryu/blob/book/ryu/app/wifi.py#L109)).**   

![](https://github.com/ramonfontes/reproducible-research/blob/master/mininet-wifi/V2X-Slicing/arq-multi-c.png)   
Figure 1. Proposed prototype for multiple controller approach
