### Requirements ###
* python-scapy
* ryu
* ofsoftswitch13


### Simple steps to reproducibility ###

##### Terminal 1: #####  
1- sudo python krack-mininet-wifi.py 

##### Terminal 2: #####   
2- git clone https://github.com/ramonfontes/ryu -b dev   
3- ~/ryu$ PYTHONPATH=. ./bin/ryu-manager ryu/app/krack_code.py ryu/app/krack_app.py  

##### Terminal 1: #####   
4- mininet-wifi>py sta1.setPosition('150,100,0')   
5- mininet-wifi>sta1 ping 10.0.0.102  
