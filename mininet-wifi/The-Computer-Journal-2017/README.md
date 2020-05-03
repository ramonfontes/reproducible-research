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