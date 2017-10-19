#!/usr/bin/python

"""This code tests if APs are affected by CVE-2017-13082 (KRACK attack) and
determine whether an implementation is vulnerable to attacks."""

__author__ = "Ramon Fontes, Hedertone Almeida, and Christian Rothenberg"
__credits__ = ["https://github.com/vanhoefm/krackattacks-test-ap-ft"]

from mininet.net import Mininet
from mininet.node import Controller, UserAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import os

def topology():

    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, accessPoint=UserAP, enable_wmediumd=True, enable_interference=True)

    print "*** Creating nodes"
    net.addStation('sta1', ip='10.0.0.1/8', position='80,80,0')
    ap1 = net.addAccessPoint('ap1', ip='10.0.0.101/8', mac='02:00:00:00:00:01', ssid="handover", mode="g", channel="1", ieee80211r='yes', mobility_domain='a1b2', passwd='123456789a', encrypt='wpa2', position='10,30,0', inNamespace=True)
    ap2 = net.addAccessPoint('ap2', ip='10.0.0.102/8', mac='02:00:00:00:00:02', ssid="handover", mode="g", channel="6", ieee80211r='yes', mobility_domain='a1b2', passwd='123456789a', encrypt='wpa2', position='60,30,0', inNamespace=True)
    ap3 = net.addAccessPoint('ap3', ip='10.0.0.103/8', mac='02:00:00:00:00:03', ssid="handover", mode="g", channel="1", ieee80211r='yes', mobility_domain='a1b2', passwd='123456789a', encrypt='wpa2', position='120,100,0', inNamespace=True)
    c1 = net.addController('c1', controller=Controller)

    print "*** Configuring Propagation Model"
    net.propagationModel("logDistancePropagationLossModel", exp=3.5)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    'plotting graph'
    net.plotGraph(min_x=-100, min_y=-100, max_x=200, max_y=200)

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])

    os.system('pkill -f "\wpa_supplicant -B -Dnl80211\"')

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
