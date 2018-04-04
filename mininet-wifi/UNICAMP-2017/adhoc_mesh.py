#!/usr/bin/python

'This example shows how to work with both wireless adhoc and wireless mesh'

from mininet.wifi.net import Mininet_wifi
from mininet.wifi.cli import CLI_wifi
from mininet.wifi.link import wmediumd, adhoc, mesh
from mininet.wifi.wmediumdConnector import interference
from mininet.log import setLogLevel


def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    print("*** Creating nodes")
    sta1 = net.addStation('sta1', position='10,10,0')
    sta2 = net.addStation('sta2', position='60,10,0')
    sta3 = net.addStation('sta3', position='100,10,0')
    sta4 = net.addStation('sta4', position='10,140,0')
    sta5 = net.addStation('sta5', position='60,140,0')
    sta6 = net.addStation('sta6', position='100,140,0')

    print("*** Configuring Propagation Model")
    net.propagationModel(model="logDistance", exp=4.5)

    print("*** Configuring wifi nodes")
    net.configureWifiNodes()

    print("*** Creating links")
    net.addLink(sta1, cls=mesh, ssid='meshNet')
    net.addLink(sta2, cls=mesh, ssid='meshNet')
    net.addLink(sta3, cls=mesh, ssid='meshNet')
    net.addLink(sta4, cls=adhoc, ssid='adhocNet')
    net.addLink(sta5, cls=adhoc, ssid='adhocNet')
    net.addLink(sta6, cls=adhoc, ssid='adhocNet')

    net.plotGraph(max_x=200, max_y=200)

    print("*** Starting network")
    net.build()

    print("*** Running CLI")
    CLI_wifi(net)

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
