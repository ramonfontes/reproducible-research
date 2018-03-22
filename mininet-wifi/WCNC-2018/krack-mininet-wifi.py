#!/usr/bin/python

"""This code tests if APs are affected by CVE-2017-13082 (KRACK attack) and
determine whether an implementation is vulnerable to attacks."""

__author__ = "Ramon Fontes, Hedertone Almeida, and Christian Rothenberg"
__credits__ = ["https://github.com/vanhoefm/krackattacks-test-ap-ft"]

from mininet.wifi.net import MininetWithControlNet
from mininet.wifi.node import UserAP
from mininet.wifi.cli import CLI_wifi
from mininet.wifi.link import wmediumd
from mininet.wifi.wmediumdConnector import interference
from mininet.node import RemoteController
from mininet.log import setLogLevel
import os


def topology():

    print("*** Shutting down any controller running on port 6653")
    os.system('sudo fuser -k 6653/tcp')

    "Create a network."
    net = MininetWithControlNet(controller=RemoteController, accessPoint=UserAP,
                       link=wmediumd, wmediumd_mode=interference,
                       inNamespace=True)

    print("*** Creating nodes")
    net.addStation('sta1', ip='10.0.0.1/8', position='20,0,0', inNamespace=False)
    net.addStation('sta2', ip='10.0.0.2/8', position='-50,-50,0', inNamespace=True)
    ap1 = net.addAccessPoint('ap1', ip='10.0.0.101/8', mac='02:00:00:00:00:01',
                             ssid="handover", mode="g", channel="1", ieee80211r='yes',
                             mobility_domain='a1b2', passwd='123456789a', encrypt='wpa2',
                             position='10,30,0', inNamespace=True)
    ap2 = net.addAccessPoint('ap2', ip='10.0.0.102/8', mac='02:00:00:00:00:02',
                             ssid="handover", mode="g", channel="6", ieee80211r='yes',
                             mobility_domain='a1b2', passwd='123456789a', encrypt='wpa2',
                             position='100,30,0', inNamespace=True)
    c1 = net.addController('c1', controller=RemoteController, port=6653)

    print("*** Configuring Propagation Model")
    net.propagationModel(model="logDistance", exp=3.5)

    print("*** Configuring wifi nodes")
    net.configureWifiNodes()

    print("*** Linking nodes")
    net.addLink(ap1, ap2)

    'plotting graph'
    net.plotGraph(min_x=-100, min_y=-100, max_x=200, max_y=200)

    print("*** Starting network")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    os.system('ip link set hwsim0 up')

    print("*** Running CLI")
    CLI_wifi(net)

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
