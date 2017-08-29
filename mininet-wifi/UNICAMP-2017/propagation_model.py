#!/usr/bin/python

'This example creates a simple network topology with 1 AP and 3 stations'

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

def topology():
    "Create a network."
    net = Mininet(enable_wmediumd=True, enable_interference=True)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', position='10,20,0')
    sta2 = net.addStation('sta2', position='40,30,0')
    sta3 = net.addStation('sta3', position='60,20,0')
    ap1 = net.addAccessPoint('ap1', ssid="my-ssid", mode="a", channel="36", failMode='standalone', position='10,10,0')

    print "*** Configuring Propagation Model"
    net.propagationModel("logDistancePropagationLossModel", exp=3.5)

    net.plotGraph(max_x=100, max_y=100)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Starting network"
    net.build()

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
