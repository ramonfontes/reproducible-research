#!/usr/bin/python

'This example shows how to work with both wireless adhoc and wireless mesh'

from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd, adhoc, mesh
from mn_wifi.wmediumdConnector import interference
from mininet.log import setLogLevel, info


def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='10,10,0')
    sta2 = net.addStation('sta2', position='60,10,0')
    sta3 = net.addStation('sta3', position='100,10,0')
    sta4 = net.addStation('sta4', position='10,140,0')
    sta5 = net.addStation('sta5', position='60,140,0')
    sta6 = net.addStation('sta6', position='100,140,0')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(sta1, cls=mesh, intf='sta1-wlan0', ssid='meshNet')
    net.addLink(sta2, cls=mesh, intf='sta2-wlan0', ssid='meshNet')
    net.addLink(sta3, cls=mesh, intf='sta3-wlan0', ssid='meshNet')
    net.addLink(sta4, cls=adhoc, intf='sta4-wlan0', ssid='adhocNet')
    net.addLink(sta5, cls=adhoc, intf='sta5-wlan0', ssid='adhocNet')
    net.addLink(sta6, cls=adhoc, intf='sta6-wlan0', ssid='adhocNet')

    net.plotGraph(max_x=200, max_y=200)

    info("*** Starting network\n")
    net.build()

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
