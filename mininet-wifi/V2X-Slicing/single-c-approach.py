#!/usr/bin/python

import os
from sys import version_info as py_version_info

from mininet.node import RemoteController
from mininet.term import makeTerm, cleanUpScreens
from mininet.log import setLogLevel
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.wmediumdConnector import interference


def topology():

    os.system('rm data-log/sta1.log')

    "Create a network."
    net = Mininet_wifi(controller=RemoteController, link=wmediumd,
                       wmediumd_mode=interference)

    print("*** Creating nodes")
    s10 = net.addSwitch('auth10')
    s11 = net.addSwitch('s11')
    s12 = net.addSwitch('s12')
    s13 = net.addSwitch('s13')
    s14 = net.addSwitch('s14')
    s17 = net.addSwitch('s17')
    s20 = net.addSwitch('mecgw20')
    sta1 = net.addStation('sta1', wlans=3, mac='00:00:00:00:00:01', ip='10.0.0.1/8',
                          radius_passwd='sdnteam', encrypt='wpa2,wpa2,', radius_identity='joe',
                          inNamespace=False)
    t1 = net.addStation('telcoA1', mac='00:00:00:00:00:03', ssid='telcoA1', type='ap',
                        authmode='8021x', encrypt='wpa2', mode='n', channel='1',
                        radius_server='192.168.0.1', position='500,600,0', range=700)
    t2 = net.addStation('telcoA2', mac='00:00:00:00:00:04', ssid='telcoA2', type='ap',
                        authmode='8021x', encrypt='wpa2', mode='n', channel='1',
                        radius_server='192.168.0.1', position='500,130,0', range=700)
    t3 = net.addStation('telcoC1', mac='00:00:00:00:00:05', ssid='telcoC1', type='ap',
                        authmode='8021x', encrypt='wpa2', mode='n', channel='11',
                        radius_server='172.16.0.1', position='500,300,0', range=400)
    t4 = net.addStation('telcoB1', mac='00:00:00:00:00:06', ssid='telcoB1', type='ap',
                        authmode='8021x', encrypt='wpa2', mode='n', channel='6',
                        radius_server='192.168.0.1', position='500,380,0', range=700)
    h1 = net.addHost('authsrv1', ip='192.168.0.1/24')
    h2 = net.addHost('h2', ip='192.168.0.100/24')
    h3 = net.addHost('h3', ip='192.168.0.100/24')
    h4 = net.addHost('h4', ip='192.168.0.100/24')
    c1 = net.addController('c1', controller=RemoteController, port=6653)

    print("*** Configuring Propagation Model")
    net.setPropagationModel(model="logDistance", exp=3.5)

    #h1.plot(position='200,600,0')
    #h2.plot(position='340,630,0')
    #h3.plot(position='350,100,0')
    #h4.plot(position='50,350,0')
    #s17.plot(position='100,300,0')
    #s11.plot(position='340,590,0')
    #s12.plot(position='340,140,0')
    #s13.plot(position='340,310,0')
    #s14.plot(position='340,370,0')
    #s10.plot(position='320,350,0')
    #s20.plot(position='180,350,0')

    #net.setModule('./mac80211_hwsim.ko')

    print("*** Configuring wifi nodes")
    net.configureWifiNodes()

    net.addLink(s11, t1, bw=1000)
    net.addLink(s12, t2, bw=1000)
    net.addLink(s13, t3, bw=1000)
    net.addLink(s14, t4, bw=1000)

    net.addLink(s11, s10)
    net.addLink(s12, s10)
    net.addLink(s13, s10)
    net.addLink(s14, s10)

    net.addLink(s11, s20, bw=100, delay='2.5ms')
    net.addLink(s12, s20, bw=100, delay='2.5ms')
    net.addLink(s13, s20, bw=100, delay='5ms')
    net.addLink(s14, s20, bw=100, delay='25ms')

    net.addLink(h2, s11, bw=100, delay='2.5ms')
    net.addLink(h3, s12, bw=100, delay='2.5ms')
    net.addLink(h4, s17)

    net.addLink(s10, h1)
    net.addLink(s20, s17)

    "plotting graph"
    net.plotGraph(max_x=700, max_y=700)

    net.startMobility(time=10)
    net.mobility(sta1, 'start', time=10, position='510.0,610.0,0.0')
    net.mobility(sta1, 'stop', time=100, position='510.0,10.0,0.0')
    net.stopMobility(time=100)

    print("*** Starting network")
    net.build()
    c1.start()
    s10.start([c1])
    s11.start([c1])
    s12.start([c1])
    s13.start([c1])
    s14.start([c1])
    s17.start([c1])
    s20.start([c1])

    sta1.setMasterMode(intf='sta1-wlan2')
    sta1.cmd('iw dev sta1-wlan2 interface add mon1 type monitor')
    sta1.cmd('ifconfig mon1 up')

    sta1.cmd('ifconfig sta1-wlan0 0')
    sta1.cmd('ifconfig sta1-wlan1 0')

    t3.cmd('ifconfig telcoC1-wlan0 192.168.100.2')

    print("\n*** Configuring network")
    t1.cmd('ifconfig telcoA1-eth1 192.168.0.201')
    t2.cmd('ifconfig telcoA2-eth1 192.168.0.202')
    t3.cmd('ifconfig telcoC1-eth1 172.16.0.203')
    t4.cmd('ifconfig telcoB1-eth1 192.168.0.204')
    t1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    t2.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    t3.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    t4.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    h1.cmd('ifconfig authsrv1-eth0:0 172.16.0.1/16')

    #Configuring radius controller info
    h1.cmd('rc.radiusd start')
    s20.cmd('ovs-ofctl add-flow mecgw20 in_port=1,actions=5')
    s20.cmd('ovs-ofctl add-flow mecgw20 in_port=5,actions=1')
    s20.cmd('ovs-ofctl add-flow mecgw20 in_port=2,actions=6')
    s20.cmd('ovs-ofctl add-flow mecgw20 in_port=6,actions=2')
    s20.cmd('ovs-ofctl add-flow mecgw20 in_port=3,actions=5')
    s20.cmd('ovs-ofctl add-flow mecgw20 in_port=5,dl_type=0x800,'
            'nw_dst=172.16.0.1,actions=3')
    s20.cmd('ovs-ofctl add-flow mecgw20 in_port=5,dl_type=0x800,'
            'nw_dst=10.0.0.1,actions=4')
    s20.cmd('ovs-ofctl add-flow mecgw20 in_port=4,actions=5')

    s11.cmd('ovs-ofctl add-flow s11 in_port=1,priority=65535,'
            'dl_type=0x800,nw_proto=17,tp_dst=1812,actions=2')
    s11.cmd('ovs-ofctl add-flow s11 in_port=2,actions=1')
    s11.cmd('ovs-ofctl add-flow s11 in_port=4,actions=1')
    s12.cmd('ovs-ofctl add-flow s12 in_port=1,priority=65535,'
            'dl_type=0x800,nw_proto=17,tp_dst=1812,actions=2')
    s12.cmd('ovs-ofctl add-flow s12 in_port=2,actions=1')
    s12.cmd('ovs-ofctl add-flow s12 in_port=4,actions=1')
    s13.cmd('ovs-ofctl add-flow s13 in_port=1,priority=65535,'
            'dl_type=0x800,nw_proto=17,tp_dst=1812,actions=2')
    s13.cmd('ovs-ofctl add-flow s13 in_port=2,actions=1')
    s13.cmd('ovs-ofctl add-flow s13 in_port=3,actions=1')
    s14.cmd('ovs-ofctl add-flow s14 in_port=1,priority=65535,'
            'dl_type=0x800,nw_proto=17,tp_dst=1812,actions=2')
    s14.cmd('ovs-ofctl add-flow s14 in_port=2,actions=1')
    s14.cmd('ovs-ofctl add-flow s14 in_port=3,actions=1')
    s10.cmd('ovs-ofctl add-flow auth10 in_port=1,priority=65535,'
            'dl_type=0x800,nw_proto=17,tp_dst=1812,actions=5,controller')
    s10.cmd('ovs-ofctl add-flow auth10 in_port=2,priority=65535,'
            'dl_type=0x800,nw_proto=17,tp_dst=1812,actions=5,controller')
    s10.cmd('ovs-ofctl add-flow auth10 in_port=3,priority=65535,'
            'dl_type=0x800,nw_proto=17,tp_dst=1812,actions=5,controller')
    s10.cmd('ovs-ofctl add-flow auth10 in_port=4,priority=65535,'
            'dl_type=0x800,nw_proto=17,tp_dst=1812,actions=5,controller')

    s11.cmd('ovs-ofctl add-flow s11 in_port=1,dl_type=0x800,'
            'nw_dst=192.168.0.100,actions=4')
    s12.cmd('ovs-ofctl add-flow s12 in_port=1,dl_type=0x800,'
            'nw_dst=192.168.0.100,actions=4')
    s13.cmd('ovs-ofctl add-flow s13 in_port=1,dl_type=0x800,'
             'nw_dst=172.16.0.100,actions=3')
    s14.cmd('ovs-ofctl add-flow s14 in_port=1,dl_type=0x800,'
             'nw_dst=192.168.0.100,actions=3')

    h2.cmd('route add -host 10.0.0.1 gw 192.168.0.201')
    h3.cmd('route add -host 10.0.0.1 gw 192.168.0.202')
    h4.cmd('route add -host 10.0.0.1 gw 192.168.0.204')
    h4.cmd('ifconfig h4-eth0:0 172.16.0.100/16')
    h4.cmd('route add -host 192.168.100.1 gw 172.16.0.203')

    s17.cmd('ovs-vsctl set Bridge s17 datapath_type=netdev')
    s17.cmd('ovs-ofctl -O Openflow13 add-meter s17 meter=1,kbps,band=type=drop,rate=5000')

    makeTerm( h2, cmd="bash -c 'iperf -s -i 1 -u;'" )
    makeTerm( h3, cmd="bash -c 'iperf -s -i 1 -u;'" )
    makeTerm( h4, cmd="bash -c 'iperf -s -i 1 -u;'" )

    print("*** Running CLI")
    CLI(net)

    os.system('pkill radiusd')
    if py_version_info < (3, 0):
        os.system('pkill -f SimpleHTTPServer')
    else:
        os.system('pkill -f http.server')
    os.system('pkill -f \"xterm -title\"')

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
