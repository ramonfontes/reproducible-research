#!/usr/bin/python

'This example creates a simple network topology with 1 AP and 3 stations'

from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference


def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    net.addStation('sta1', position='10,20,0')
    net.addStation('sta2', position='40,30,0')
    net.addStation('sta3', position='60,20,0')
    net.addAccessPoint('ap1', ssid="my-ssid", mode="a", channel="36",
                       failMode='standalone', position='10,10,0')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3.9)

    net.plotGraph(max_x=100, max_y=100)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Starting network\n")
    net.build()

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
