#!/usr/bin/python

'Example for Handover'

from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI_wifi
from mininet.log import setLogLevel, info


def topology():

    "Create a network."
    net = Mininet_wifi(accessPoint=OVSKernelAP)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8')
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1',
                             failMode='standalone', position='15,30,0')
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='6',
                             failMode='standalone', position='55,30,0')

    net.propagationModel(model='logDistance', exp=5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, ap2)
    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)

    'plotting graph'
    net.plotGraph(max_x=100, max_y=100)

    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=1, position='10,30,0')
    net.mobility(sta2, 'start', time=2, position='10,40,0')
    net.mobility(sta1, 'stop', time=30, position='60,30,0')
    net.mobility(sta2, 'stop', time=10, position='25,40,0')
    net.stopMobility(time=40)

    info("*** Starting network\n")
    net.build()

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
