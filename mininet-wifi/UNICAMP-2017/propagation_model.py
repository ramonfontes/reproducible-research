#!/usr/bin/python

'This example creates a simple network topology with 1 AP and 3 stations'

from mininet.wifi.net import Mininet_wifi
from mininet.wifi.cli import CLI_wifi
from mininet.log import setLogLevel
from mininet.wifi.link import wmediumd
from mininet.wifi.wmediumdConnector import interference


def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    print("*** Creating nodes")
    net.addStation('sta1', position='10,20,0')
    net.addStation('sta2', position='40,30,0')
    net.addStation('sta3', position='60,20,0')
    net.addAccessPoint('ap1', ssid="my-ssid", mode="a", channel="36",
                       failMode='standalone', position='10,10,0')

    print("*** Configuring Propagation Model")
    net.propagationModel(model="logDistance", exp=4)

    net.plotGraph(max_x=100, max_y=100)

    print("*** Configuring wifi nodes")
    net.configureWifiNodes()

    print("*** Starting network")
    net.build()

    print("*** Running CLI")
    CLI_wifi(net)

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
