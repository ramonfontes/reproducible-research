#!/usr/bin/python

'Example for handover'

from mininet.log import setLogLevel
from mininet.node import Controller, OVSKernelSwitch
from mininet.wifi.node import OVSKernelAP
from mininet.wifi.cli import CLI_wifi
from mininet.wifi.net import Mininet_wifi


def topology():

    "Create a network."
    net = Mininet_wifi(controller=Controller, switch=OVSKernelSwitch, accessPoint=OVSKernelAP)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid1', mode='g', channel='1', position='15,30,0')
    ap2 = net.addAccessPoint('ap2', ssid='new-ssid1', mode='g', channel='6', position='55,30,0')
    s3 = net.addSwitch('s3')
    h1 = net.addHost('h1', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
    c1 = net.addController('c1', controller=Controller, port=6653)

    net.propagationModel(model="logDistance", exp=4.3)

    print "*** Configuring WiFi Nodes"
    net.configureWifiNodes()

    h1.plot(position='35,90,0')
    s3.plot(position='35,80,0')

    print "*** Creating links"
    net.addLink(ap1, s3)
    net.addLink(ap2, s3)
    net.addLink(h1, s3)

    'plotting graph'
    net.plotGraph(max_x=100, max_y=100)

    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=1, position='10,30,0')
    net.mobility(sta1, 'stop', time=80, position='60,30,0')
    net.stopMobility(time=80)

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    s3.start([c1])

    print "*** Running CLI"
    CLI_wifi(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
