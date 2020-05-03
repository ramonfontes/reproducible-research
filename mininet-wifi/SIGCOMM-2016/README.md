## Reproducibility Steps

### Requirements
- Mininet-WiFi
- WiFi interface + (second WiFi or ethernet interface)
- Floodlight
- ofsoftswitch13
- speedtest-cli

**Note** - You may want to set both Internet and wlan interfaces in `hybridVirtualPhysical.py`.

```
internetIface ='eth0'# wired/wireless card.
usbDongleIface ='wlan0'# wifi interface.
```

Now, run the Floodlight controller

```
sudo java -jar target/floodlight.jar
```

Then, run the network topology in a 2nd terminal:

```
sudo py hybridVirtualPhysical.py
mininet-wifi> sh ./rule.hybridVirtualPhysical
```

Despite the content of `rule.hybridVirtualPhysical` is included in `hybridVirtualPhysical.py`, we have faced some problems with floodlight. Thus, probably you have to run `rule.hybridVirtualPhysical` after running `hybridVirtualPhysical.py`.


Now, stations should be able to communicate with to each other as well as to the Internet. Now, you may consider to use any station and run `speedtest-cli`:

```
mininet-wifi>xterm sta1
```

sta1's terminal: 
```
speedtest-cli
```

There is a web server accessible at 10.0.0.111 and according rules added in `rule.hybridVirtualPhysical` if you access 10.0.0.109 the traffic will be redirect to 10.0.0.111.


**Useful commands**
```
sta1 iw dev sta1-wlan0 mpath dump #verify mesh routing information
dpctl unix:/tmp/ap3 stats-flow
dpctl unix:/tmp/ap3 stats-meter
dpctl unix:/tmp/ap3 meter-config
```

### bibtex:
@inproceedings{fontes2016mininet,  
  title={Mininet-WiFi: A Platform for Hybrid Physical-Virtual Software-Defined Wireless Networking Research},  
  author={Fontes, Ramon dos Reis and Rothenberg, Christian Esteve},  
  booktitle={Proceedings of the 2016 conference on ACM SIGCOMM 2016 Conference},  
  pages={607--608},  
  year={2016},  
  organization={ACM}  
}
