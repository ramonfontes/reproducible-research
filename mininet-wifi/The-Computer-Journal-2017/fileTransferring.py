#!/usr/bin/python

"""Code created to be presented with the paper titled:
   "How far can we go? Towards Realistic Software-Defined Wireless Networking Experiments" 
   authors: Ramon dos Reis Fontes and Christian Esteve Rothenberg"""

"""Topology

   Nodes:   sta1------ap3---------sta2
   Distance: |--2.72m--|---4.08m---|"""


from mininet.log import setLogLevel
from mininet.node import Controller
from mininet.wifi.net import Mininet_wifi
from mininet.wifi.cli import CLI_wifi


def topology():

    "Create a network."
    net = Mininet_wifi( controller=Controller )

    print("*** Creating nodes")
    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:01',
                           ip='192.168.0.1/24', position='47.28,50,0' )
    sta2 = net.addStation( 'sta2', mac='00:00:00:00:00:02',
                           ip='192.168.0.2/24', position='54.08,50,0' )
    ap3 = net.addAccessPoint( 'ap3', ssid='ap-ssid3', mode='b', channel='1',
                              position='50,50,0' )
    c4 = net.addController( 'c4', controller=Controller, port=6653 )

    print("*** Configuring wifi nodes")
    net.configureWifiNodes()

    net.plotGraph(max_x=100, max_y=100)

    print("*** Associating and Creating links")
    net.addLink(sta1, ap3)
    net.addLink(sta2, ap3)

    print("*** Starting network")
    net.build()
    c4.start()
    ap3.start( [c4] )

    sta2.cmd('pushd /home/alpha/Downloads; python3 -m http.server 80 &')

    print("*** Running CLI")
    CLI_wifi( net )

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
