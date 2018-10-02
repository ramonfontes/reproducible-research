#!/usr/bin/python

"This example shows how work with wireless and wired media"

from mininet.log import setLogLevel, info
from mininet.node import Controller
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi


def topology():
    "Create a network."
    net = Mininet_wifi( controller=Controller )

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint( 'ap1', ssid="simplewifi", mode="g", channel="5" )
    sta1 = net.addStation( 'sta1', ip='192.168.0.1/24' )
    sta2 = net.addStation( 'sta2', ip='192.168.0.2/24' )
    h3 = net.addHost( 'h3', ip='192.168.0.3/24' )
    h4 = net.addHost( 'h4', ip='192.168.0.4/24' )
    c0 = net.addController('c0')

    net.configureWifiNodes()

    info("*** Adding Link\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)
    net.addLink(h3, ap1)
    net.addLink(h4, ap1)

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start( [c0] )

    info("*** Running CLI\n")
    CLI_wifi( net )

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
