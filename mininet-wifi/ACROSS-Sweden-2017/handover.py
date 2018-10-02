#!/usr/bin/python

'Example for handover'

from mininet.log import setLogLevel, info
from mininet.node import Controller
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi


def topology():

    "Create a network."
    net = Mininet_wifi(controller=Controller)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid1', mode='g', channel='1', position='15,30,0')
    ap2 = net.addAccessPoint('ap2', ssid='new-ssid1', mode='g', channel='6', position='55,30,0')
    s3 = net.addSwitch('s3')
    h1 = net.addHost('h1', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
    c1 = net.addController('c1')

    net.setPropagationModel(model="logDistance", exp=4.3)

    info("*** Configuring WiFi Nodes\n")
    net.configureWifiNodes()

    h1.plot(position='35,90,0')
    s3.plot(position='35,80,0')

    info("*** Creating links\n")
    net.addLink(ap1, s3)
    net.addLink(ap2, s3)
    net.addLink(h1, s3)

    net.plotGraph(max_x=100, max_y=100)

    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=1, position='10,30,0')
    net.mobility(sta1, 'stop', time=80, position='60,30,0')
    net.stopMobility(time=80)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    s3.start([c1])

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
