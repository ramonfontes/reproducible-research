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
* `sudo python use-case.py` 

**Terminal 2**
* `git clone https://github.com/ramonfontes/ryu -b dev`    
* `cd ryu`   
* ~/ryu$ `PYTHONPATH=. ./bin/ryu-manager ryu/app/vanet_run.py ryu/app/simple_switch_13.py`     

**Extract dataset from data-log/sta1.log**   
**>> you have to modify [vanet_run.py](https://github.com/ramonfontes/ryu/blob/dev/ryu/app/vanet_run.py#L134) in order to run the correct case.**



