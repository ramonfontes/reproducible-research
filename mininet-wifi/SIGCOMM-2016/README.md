
### Requirements
- Mininet-WiFi
- WiFi interface + (other WiFi or ethernet interface)
- Floodlight OpenFlow controller
- ofsoftswitch13 (you may install it with util/install.sh -3f) - https://github.com/CPqD/ofsoftswitch13
- Speedtest-cli
- You have to set both Internet and wlan interfaces in hybridVirtualPhysical.py
  - internetIface = 'eth0' # wired/wireless card.
  - usbDongleIface = 'wlan0' # wifi interface.

### Reproducibility Steps
- Terminal 1
  - ~/floodlight$ sudo java -jar target/floodlight.jar
  
- Terminal 2
  - ~/reproducible-research/mininet-wifi/SIGCOMM-2016$ sudo python hybridVirtualPhysical.py
  - mininet-wifi> sh ./rule.hybridVirtualPhysical

Now, stations should be able to communicate with each other and with the Internet. You may use any station connected to any Access Point and try it out: 
  - mininet-wifi> xterm $station
  - $station> speedtest-cli
  
Using speedtest-cli you can test both Download and Upload speed of your Internet connection. The available bandwidth is controlled by OpenFlow meter entries. There is a web server accessible at 10.0.0.111 and according rules applied in rule.hybridVirtualPhysical, if you access 10.0.0.109 the traffic will be redirect to 10.0.0.111.

**Useful commands:**  
sta1 iw dev sta1-wlan0 mpath dump #verify mesh routing information  
sh dpctl unix:/tmp/ap3 stats-flow  
sh dpctl unix:/tmp/ap3 stats-meter  
sh dpctl unix:/tmp/ap3 meter-config  

### bibtex:
@inproceedings{fontes2016mininet,  
  title={Mininet-WiFi: A Platform for Hybrid Physical-Virtual Software-Defined Wireless Networking Research},  
  author={Fontes, Ramon dos Reis and Rothenberg, Christian Esteve},  
  booktitle={Proceedings of the 2016 conference on ACM SIGCOMM 2016 Conference},  
  pages={607--608},  
  year={2016},  
  organization={ACM}  
}
