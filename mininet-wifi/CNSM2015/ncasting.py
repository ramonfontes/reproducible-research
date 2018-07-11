#!/usr/bin/python


import subprocess
import os

from mininet.node import  RemoteController, OVSKernelSwitch
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi

"""      ap1.
         /    .
        /       .
h1----s1        sta1
       \       .
        \    .
        ap2."""

def topology():
    "Create a network."
    net = Mininet_wifi( controller=RemoteController, link=TCLink,
                        switch=OVSKernelSwitch, accessPoint=OVSKernelAP )

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint( 'ap1', ssid="ssid_1", mode="g", channel="5" )
    ap2 = net.addAccessPoint( 'ap2', ssid="ssid_2", mode="g", channel="11" )
    sta3 = net.addStation( 'sta3', ip="192.168.0.100/24", wlans=2 )
    h4 = net.addHost( 'h4', ip="192.168.0.1/24", mac="00:00:00:00:00:04" )
    s5 = net.addSwitch( 's5' )
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653 )

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Adding Link\n")
    net.addLink(h4, s5, bw=1000)
    net.addLink(ap1, s5, bw=1000)
    net.addLink(ap2, s5, bw=1000)
    net.addLink(ap1, sta3)
    net.addLink(sta3, ap2)

    info("*** Starting network\n")
    net.build()
    c0.start()
    s5.start( [c0] )
    ap1.start( [c0] )
    ap2.start( [c0] )

    sta3.cmd("ifconfig sta3-wlan1 192.168.1.100/24 up")
    h4.cmd("ifconfig h4-eth0:0 192.168.1.1/24")

    info("*** Running CLI\n")
    CLI_wifi( net )

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
