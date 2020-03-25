#!/usr/bin/python

"""Code created to be presented with the paper titled:
   "How far can we go? Towards Realistic Software-Defined Wireless Networking Experiments" 
   authors: Ramon dos Reis Fontes and Christian Esteve Rothenberg"""

"""Topology

   Nodes:   sta1------ap3---------sta2
   Distance: |--2.72m--|---4.08m---|"""


from mininet.log import setLogLevel, info
from mininet.node import Controller
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI


def topology():

    "Create a network."
    net = Mininet_wifi( controller=Controller )

    info("*** Creating nodes\n")
    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:01',
                           ip='192.168.0.1/24', position='47.28,50,0' )
    sta2 = net.addStation( 'sta2', mac='00:00:00:00:00:02',
                           ip='192.168.0.2/24', position='54.08,50,0' )
    ap1 = net.addAccessPoint( 'ap3', ssid='ap-ssid', mode='b', channel='1',
                              position='50,50,0' )
    c1 = net.addController( 'c1' )

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    net.plotGraph(max_x=100, max_y=100)

    info("*** Associating and Creating links\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start( [c1] )

    sta2.cmd('pushd /home/alpha/Downloads; python3 -m http.server 80 &')

    info("*** Running CLI\n")
    CLI( net )

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
