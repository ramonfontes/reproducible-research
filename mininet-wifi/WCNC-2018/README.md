**Simple steps to reproducibility**

***Terminal 1:***  
1- sudo python krack-mininet-wifi.py 

***Terminal 2:***     
2- PYTHONPATH=. ./bin/ryu-manager ryu/app/krack_run.py ryu/app/krack_app.py  

***Terminal 1:***   
3- mininet-wifi>xterm sta1   
4- sta1 terminal: wpa_cli -i sta1-wlan0   
5- sta1 terminal: roam 02:00:00:00:00:02   
