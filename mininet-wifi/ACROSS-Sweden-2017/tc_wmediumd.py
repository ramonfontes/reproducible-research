#!/usr/bin/python

'Starting a topology with and without wmediumd'

from mininet.log import setLogLevel
from mininet.node import Controller
from mininet.wifi.net import Mininet_wifi
from mininet.wifi.node import UserAP
from mininet.wifi.cli import CLI_wifi
import sys


def topology(wmediumd):

    "Create a network."
    if wmediumd:
        net = Mininet_wifi(controller=Controller, accessPoint=UserAP, enable_wmediumd=True, enable_interference=True)
    else:
        net = Mininet_wifi(controller=Controller, accessPoint=UserAP)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8', position='120,140,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:02', ip='10.0.0.2/8', position='10,30,0')
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:03', ip='10.0.0.3/8', position='10,50,0')
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1', position='15,30,0', ieee80211r='yes', mobility_domain='a1b2', passwd='123456789a', encrypt='wpa2')
    c1 = net.addController('c1', controller=Controller)

    print "*** Configuring Propagation Model"
    net.propagationModel(model="logDistance", exp = 4.2)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    'plotting graph'
    net.plotGraph(max_x=150, max_y=150)

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start([c1])

    print "*** Running CLI"
    CLI_wifi(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    wmediumd = True if '-w' in sys.argv else False
    topology(wmediumd)
