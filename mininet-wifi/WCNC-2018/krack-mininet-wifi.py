#!/usr/bin/python

"""This code tests if APs are affected by CVE-2017-13082 (KRACK attack) and
determine whether an implementation is vulnerable to attacks."""

__author__ = "Ramon Fontes, Hedertone Almeida, and Christian Rothenberg"
__credits__ = ["https://github.com/vanhoefm/krackattacks-test-ap-ft"]

from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from mn_wifi.net import MininetWithControlWNet
from mn_wifi.node import UserAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
import os


def topology():

    info("*** Shutting down any controller running on port 6653\n")
    os.system('sudo fuser -k 6653/tcp')

    "Create a network."
    net = MininetWithControlWNet(controller=RemoteController, accessPoint=UserAP,
                                 link=wmediumd, wmediumd_mode=interference,
                                 inNamespace=True)

    info("*** Creating nodes\n")
    net.addStation('sta1', ip='10.0.0.1/8', position='20,0,0', inNamespace=False,
                   scan_freq='2412', freq_list='2412')
    ap1 = net.addAccessPoint('ap1', mac='02:00:00:00:00:01',
                             ssid='handover', mode='g', channel='1', ieee80211r='yes',
                             mobility_domain='a1b2', passwd='123456789a', encrypt='wpa2',
                             position='10,30,0', inNamespace=True)
    ap2 = net.addAccessPoint('ap2', mac='02:00:00:00:00:02',
                             ssid='handover', mode='g', channel='1', ieee80211r='yes',
                             mobility_domain='a1b2', passwd='123456789a', encrypt='wpa2',
                             position='100,30,0', inNamespace=True)
    c1 = net.addController('c1', controller=RemoteController, port=6653)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Linking nodes\n")
    net.addLink(ap1, ap2)

    'plotting graph'
    net.plotGraph(min_x=-100, min_y=-100, max_x=200, max_y=200)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    ap1.setIP('10.0.0.101/8', intf='ap1-wlan1')
    ap2.setIP('10.0.0.102/8', intf='ap2-wlan1')
    os.system('ip link set hwsim0 up')

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
