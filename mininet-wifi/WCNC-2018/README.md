### Simple steps to reproducibility ###

##### Terminal 1: #####  
1- sudo python krack-mininet-wifi.py 

##### Terminal 2: #####   
2- git clone https://github.com/ramonfontes/ryu -b dev   
3- PYTHONPATH=. ./bin/ryu-manager ryu/app/krack_code.py ryu/app/krack_app.py  

##### Terminal 1: #####   
4- mininet-wifi>py sta1.setPosition('150,100,0') 
