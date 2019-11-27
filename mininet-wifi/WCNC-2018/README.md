### Requirements ###
* python-scapy
* ryu
* ofsoftswitch13

### Reproducibility Steps ###

##### Terminal 1: #####  
```
sudo python krack-mininet-wifi.py 
```

##### Terminal 2: #####   
```
git clone https://github.com/ramonfontes/ryu -b dev   
~/ryu$ sudo PYTHONPATH=. ./bin/ryu-manager ryu/app/krack_code.py ryu/app/krack_app.py  
```

##### Terminal 1: #####   
```
mininet-wifi>py sta1.setPosition('150,100,0')   
mininet-wifi>sta1 ping 10.0.0.102  
```

#### bibtex:
@article{fontesonthekrackattack,  
  title={On the Krack Attack: Reproducing Vulnerability and a Software-Defined Mitigation Approach},  
  author={Fontes, Ramon dos Reis and Rothenberg, Christian Esteve},  
  year={2017},  
  organization={WCNC}  
}
