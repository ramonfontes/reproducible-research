### Requirements to reproduce the results of this work:
* Mininet-WiFi  
* Further requirements are installed when you install Mininet-WiFi.  

### How to reproduce this work:
* Run the code with **python code.py**

### You might be interested in define different number of nodes for single and linear topos:
* If so, please define the number of nodes in **nr_nodes_single** and **nr_nodes_linear**

### You might be interested in define the number of repetitions:
* If so, please define the number of repetitions in **repetitions**

### Server and software specifications of the deployment environment (it refers the results presented into the eps files):

* **Server**:	Lenovo ThinkServer RD640  
* **Memory**:	24 GB  
* **CPU**:	12-core 2.10GHz Intel Xeon E5-2620 v2  
* **OS**:	Ubuntu 16.04 x86-64  
* **Kernel**:	4.8.0-41-generic  
* **Mininet-WiFi**:	2.0r2  
* **Open vSwitch**:	2.5.0  
* **OpenFlow Reference Implementation**:	1.0.0  

### Please note that the code available at this page includes an extra test:   
The extra test is about sending data over ICMP with ping between two nodes, where the nodes (sta1 and sta2) are associated to the first two access points. The idea is to identify the impact of the consumed memory in the final results of the ping response time.   

