#!/usr/bin/python

import time
import os

from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mininet.term import makeTerm, cleanUpScreens
from mn_wifi.wmediumdConnector import interference


def topology():
    "Create a network."
    net = Mininet_wifi(controller=RemoteController,
                       link=wmediumd,
                       wmediumd_mode=interference
                       )

    ip_c0 = '172.17.0.2'
    ip_c1 = '172.17.0.3'
    ip_c2 = '172.17.0.4'

    info("*** Creating nodes\n")
    cars = []
    car1 = net.addStation('car1', mac='02:00:00:00:00:01', position='40,40,0') #, active_scan=1)
    cars.append(car1)
    for idx in range(2,11):
        cars.append(net.addStation('car%s' % idx, mac='02:00:00:00:00:%02d' % idx,
                                   position='17%s,%s,0' % (idx, (int(idx)+50)))) #, active_scan=1)

    enb1 = net.addAccessPoint('enb1', mac='00:00:00:00:00:01', ssid="handover",
                              mode="g", channel="1", datapath='user',
                              passwd='123456789a', encrypt='wpa2', ieee80211r='yes', mobility_domain='a1b2',
                              dpid='1', position='50,50,0')
    enb2 = net.addAccessPoint('enb2', mac='00:00:00:00:00:02', ssid="handover",
                              mode="g", channel="6", datapath='user',
                              passwd='123456789a', encrypt='wpa2', ieee80211r='yes', mobility_domain='a1b2',
                              dpid='2', position='110,50,0', color='r')
    enb3 = net.addAccessPoint('enb3', mac='00:00:00:00:00:03', ssid="handover",
                              mode="g", channel="11", datapath='user',
                              passwd='123456789a', encrypt='wpa2', ieee80211r='yes', mobility_domain='a1b2',
                              dpid='3', position='130,50,0')
    backbone1 = net.addSwitch('backbone1', mac='00:00:00:00:00:04', dpid='4',
                              failMode='standalone')
    server1 = net.addHost('server1', ip='10.0.0.100/8')
    c0 = net.addController('c0', port=6653, ip=ip_c0)
    c1 = net.addController('c1', port=6653, ip=ip_c1)
    c2 = net.addController('c2', port=6653, ip=ip_c2)

    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    c0.plot(position='50,80,0')
    c1.plot(position='110,80,0')
    c2.plot(position='130,80,0')
    backbone1.plot(position='110,30,0')
    server1.plot(position='110,10,0')

    info("*** Associating Stations\n")
    net.addLink(backbone1, enb1)
    net.addLink(backbone1, enb2)
    net.addLink(backbone1, enb3, delay='5ms')
    net.addLink(backbone1, server1)

    net.plotGraph(max_x=200, max_y=200)

    info("*** Starting network\n")
    net.build()
    net.addNAT().configDefault()
    enb1.start([c0])
    enb2.start([c1])
    enb3.start([c2])
    backbone1.start([])

    cars[0].cmd('iw dev %s-wlan0 interface '
                'add %s-mon0 type monitor'
                % (cars[0].name, cars[0].name))
    cars[0].cmd('ifconfig %s-mon0 up' % cars[0].name)

    enb1.cmd('ovs-ofctl add-flow "enb1" in_port=1,udp,tp_src=8000,actions=controller')
    enb2.cmd('ovs-ofctl add-flow "enb2" in_port=1,udp,tp_src=8000,actions=controller')
    enb3.cmd('ovs-ofctl add-flow "enb3" in_port=1,udp,tp_src=8000,actions=controller')
    makeTerm(cars[0], cmd="bash -c 'ping 10.0.0.100 -c200 > ping.txt;'")
    cars[0].cmd('./%s.py &' % cars[0].name)

    currentTime = time.time()
    i = 60
    j = 0
    while j<3:
        if (time.time() - currentTime) >= i:
            currentTime = time.time()
            if j == 0:
                cars[0].setPosition('100,50,0')
            else:
                cars[0].setPosition('140,50,0')
            j+=1

    info("*** Running CLI\n")
    CLI_wifi(net)

    os.system('pkill -f \"xterm -title\"')

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
