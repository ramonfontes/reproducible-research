#!/usr/bin/python

"Propagation Model Demo"

from mininet.log import setLogLevel
from mininet.node import Controller, OVSKernelSwitch
from mininet.wifi.net import Mininet_wifi
from mininet.wifi.cli import CLI_wifi
import time


def topology():
    "Create a network."
    net = Mininet_wifi( controller=Controller, switch=OVSKernelSwitch )

    print "*** Creating nodes"
    ap1 = net.addAccessPoint( 'ap1', ssid="ssid_ap1",
                              txpower=15, mode="g", channel=1, position="10,10,0" )
    sta1 = net.addStation( 'sta1', ip='192.168.0.1/24', txpower=15, position='10,10,0' )
    sta2 = net.addStation( 'sta2', ip='192.168.0.2/24', txpower=15, position='11.36,10,0' )

    net.propagationModel(model='logDistance', exp=3, sL=1)
    # net.propagationModel('ITUPropagationLossModel', pL=50)
    # net.propagationModel('twoRayGroundPropagationLossModel')
    # net.propagationModel('friisPropagationLossModel', sL=2)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Adding Link"
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)

    print "*** Starting network"
    net.build()

    for i in range(1,8):
        x = 10+i*1.36
        y = 10
        z = 0
        pos = '%s,%s,%s' % (x,y,z)
        sta1.moveStationTo(pos)
        print sta1.params['rssi'][0] 

    print "*** Running CLI"
    CLI_wifi( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
