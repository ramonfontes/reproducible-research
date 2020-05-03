## Reproducibility Steps - Wireless n-Casting

### Requirements
- Mininet-WiFi
- Floodlight Controller


To reproduce this case please follow the instructions below:

Firstly, run the controller:

```
sudo java -jar target/floodlight.jar
```

Then, start the network in a new terminal
``` 
sudo python ncasting.py
```

and install the rules from a 3rd terminal:
```
sudo python ncasting-controller.py
```


## Reproducibility Steps - MPTCP case

### Requirements
- Mininet-WiFi
- MPTCP
- ifstat
- Pox

In order to allow the communication we use pox controller with spanning tree enabled. The command below can be used to enable spanning tree:
```
./pox.py forwarding.l2_learning openflow.spanning_tree --hold-down log.level --DEBUG samples.pretty_log openflow.discovery host_tracker info.packet_dump

```
Then, start the network topology in a new terminal:
``` 
sudo python mptcp.pymininet-wifi>xterm sta1 sta1 h10 h10
```

and run some commands with xterm:

h10`s terminal #1
``` 
ifstat
```

h10`s terminal #2
``` 
iperf -s
```

sta1`s terminal #1
``` 
ifstat
```

sta1`s terminal #2
``` 
iperf -c 192.168.1.254
```

## Reproducibility Steps - Hybrid Physical-Virtual Environment

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


## Reproducibility Steps - SSID-based Flow Abstraction

### Requirements
- Mininet-WiFi
- ofsoftswitch13

To reproduce this case you have to run the following script:

```
sudo python forwardingBySSID.py
```

Then, you may run any application (e.g., Iperf) to measure the bandwidth. Alternatively, you may run `dpctl` to check the meter table configuration.


```
mininet-wifi> sh dpctl unix:/tmp/ap1 meter-config
```


## Reproducibility Steps - Propagation Model

### Requirements
- Mininet-WiFi

Consider to run `propagationModelCase.py` if you want to reproduce this case.


## Reproducibility Steps - Simple File Transfer

### Requirements
- Mininet-WiFi

Consider to run `fileTransferring.py` and `fileTransferring.c` if you want to reproduce this case.



## Reproducibility Steps - Replaying Network Conditions

### Requirements
- Mininet-WiFi

Consider to run files in the `replayingNetwork/` directory if you want to reproduce the results.