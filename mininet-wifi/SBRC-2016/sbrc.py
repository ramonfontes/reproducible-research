#!/usr/bin/python

"""Code created to be presented with the paper titled:
   "Rich Experimentation through Hybrid Physical-Virtual Software-Defined Wireless
   Networking Emulation"
   authors: Ramon dos Reis Fontes and Christian Esteve Rothenberg"""

from mininet.log import setLogLevel, info
from mininet.node import Controller, Node
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.wmediumdConnector import interference
from mn_wifi.link import wmediumd, mesh


def topology():

    "Create a network."
    net = Mininet_wifi( controller=Controller, link=wmediumd,
                        wmediumd_mode=interference)
    staList = []

    info("*** Creating nodes\n")
    for n in range(10):
        staList.append(n)
        staList[n] = net.addStation(
            'sta%s' % (n+1), wlans=2, mac='00:00:00:00:00:' + '%02x' % (n+1),
            ip='192.168.0.%s/24' % (n+1))
    phyap1 = net.addPhysicalBaseStation(
        'phyap1', ssid='SBRC16-MininetWiFi,SBRC16-MininetWiFi', mode='g', channel='1',
        wlans=2, position='50,115,0', phywlan='wlan2')
    net.addStation( 'sta11', ip='10.0.0.111/8', position='120,200,0')
    ap2 = net.addAccessPoint( 'ap2', ssid='ap2', mode='g', channel='11', position='100,175,0' )
    ap3 = net.addAccessPoint( 'ap3', ssid='ap3', mode='g', channel='6', position='150,50,0' )
    ap4 = net.addAccessPoint( 'ap4', ssid='ap4', mode='g', channel='1', position='175,150,0' )
    c1 = net.addController('c1')
    Node( 'root', inNamespace=False )

    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes")
    net.configureWifiNodes()

    'plotting graph'
    net.plotGraph(max_x=220, max_y=220)

    'Seed'
    net.seed(20)

    info("*** Associating and Creating links\n")
    for sta in staList:
        net.addLink(sta, cls=mesh, ssid='meshNet')
    net.addLink(phyap1, ap2)
    net.addLink(ap2, ap3)
    net.addLink(ap3, ap4)

    net.startMobility(time=0, model='RandomWalk', max_x=220, max_y=220, min_v=0.1, max_v=0.2)

    info("*** Starting network\n")
    net.build()
    c1.start()
    phyap1.start( [c1] )
    ap2.start( [c1] )
    ap3.start( [c1] )
    ap4.start( [c1] )

    ip = 201
    for sta in staList:
        sta.setIP('10.0.0.%s/8' % ip, intf="%s-wlan1" % sta)
        ip+=1

    info("*** Running CLI\n")
    CLI( net )

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
