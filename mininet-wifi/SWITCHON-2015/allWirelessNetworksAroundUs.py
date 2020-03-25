#!/usr/bin/python

"This example is based on this video: https://www.youtube.com/watch?v=_C4H2gBdyQY"

from mininet.node import Controller, OVSKernelSwitch
from mininet.log import setLogLevel, info
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
import os


def topology():
    "Create a network."
    net = Mininet_wifi( controller=Controller, switch=OVSKernelSwitch,
                        accessPoint=OVSKernelAP )

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', wlans=2, ip='10.0.0.2/8', max_x=120, max_y=50,
                           min_v=1.4, max_v=1.6)
    h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8' )
    ap1 = net.addAccessPoint( 'ap1', ssid='ssid_ap1', mode='g',
                              channel=6, position='70,25,0' )
    ap2 = net.addAccessPoint( 'ap2', ssid='ssid_ap2', mode='g',
                              channel=1, position='30,25,0' )
    ap3 = net.addAccessPoint( 'ap3', ssid='ssid_ap3', mode='g',
                              channel=11, position='110,25,0' )
    s4 = net.addSwitch( 's4', mac='00:00:00:00:00:10' )
    c1 = net.addController( 'c1', controller=Controller )

    net.setPropagationModel(model="logDistance", exp=4.3)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.addLink(ap1, s4)
    net.addLink(ap2, s4)
    net.addLink(ap3, s4)
    net.addLink(s4, h1)

    sta1.cmd('modprobe bonding mode=3')
    sta1.cmd('ip link add bond0 type bond')
    sta1.cmd('ip link set bond0 address 02:01:02:03:04:08')
    sta1.cmd('ip link set sta1-wlan0 down')
    sta1.cmd('ip link set sta1-wlan0 address 00:00:00:00:00:11')
    sta1.cmd('ip link set sta1-wlan0 master bond0')
    sta1.cmd('ip link set sta1-wlan1 down')
    sta1.cmd('ip link set sta1-wlan1 address 00:00:00:00:00:12')
    sta1.cmd('ip link set sta1-wlan1 master bond0')
    sta1.cmd('ip addr add 10.0.0.10/8 dev bond0')
    sta1.cmd('ip link set bond0 up')

    'plotting graph'
    net.plotGraph(max_x=140, max_y=140)

    net.startMobility(time=0, seed=1, model='RandomDirection')

    info("*** Starting network\n")
    net.build()
    c1.start()
    s4.start( [c1] )
    ap1.start( [c1] )
    ap2.start( [c1] )
    ap3.start( [c1] )

    sta1.cmd('ip addr del 10.0.0.2/8 dev sta1-wlan0')
    os.system('ovs-ofctl add-flow s4 actions=normal')

    info("*** Running CLI\n")
    CLI( net )

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
