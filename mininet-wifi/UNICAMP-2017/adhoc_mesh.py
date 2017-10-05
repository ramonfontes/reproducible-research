#!/usr/bin/python

'This example shows how to work with both wireless adhoc and wireless mesh'

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

def topology():
    "Create a network."
    net = Mininet(enable_wmediumd=True, enable_interference=True)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', position='10,10,0')
    sta2 = net.addStation('sta2', position='60,10,0')
    sta3 = net.addStation('sta3', position='100,10,0')
    sta4 = net.addStation('sta4', position='10,140,0')
    sta5 = net.addStation('sta5', position='60,140,0')
    sta6 = net.addStation('sta6', position='100,140,0')

    print "*** Configuring Propagation Model"
    net.propagationModel("logDistancePropagationLossModel", exp=4.5)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addMesh(sta1, ssid='meshNet')
    net.addMesh(sta2, ssid='meshNet')
    net.addMesh(sta3, ssid='meshNet')
    net.addHoc(sta4, ssid='adhocNet')
    net.addHoc(sta5, ssid='adhocNet')
    net.addHoc(sta6, ssid='adhocNet')

    net.plotGraph(max_x=200, max_y=200)

    print "*** Starting network"
    net.build()

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
