#!/usr/bin/python

"Propagation Model Demo"

from mininet.log import setLogLevel, info
from mininet.node import Controller
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI_wifi


def topology():
    "Create a network."
    net = Mininet_wifi( controller=Controller, accessPoint=OVSKernelAP )

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint( 'ap1', ssid="ssid_ap1",
                              txpower=15, mode="g", channel=1, position="10,10,0" )
    sta1 = net.addStation( 'sta1', ip='192.168.0.1/24', txpower=15,
                           position='10,10,0' )
    sta2 = net.addStation( 'sta2', ip='192.168.0.2/24', txpower=15,
                           position='11.36,10,0' )

    net.propagationModel(model='logDistance', exp=3, sL=1)
    # net.propagationModel('ITUPropagationLossModel', pL=50)
    # net.propagationModel('twoRayGroundPropagationLossModel')
    # net.propagationModel('friisPropagationLossModel', sL=2)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Adding Link\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)

    info("*** Starting network\n")
    net.build()

    for i in range(1,8):
        x = 10+i*1.36
        y = 10
        z = 0
        pos = '%s,%s,%s' % (x,y,z)
        sta1.setPosition(pos)
        info(sta1.params['rssi'][0])

    info("*** Running CLI\n")
    CLI_wifi( net )

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
