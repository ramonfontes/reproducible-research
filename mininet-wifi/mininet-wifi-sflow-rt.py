#!/usr/bin/python

'sflow-RT based code'

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from json import dumps
from requests import put
from mininet.util import quietRun
from os import listdir, environ
import re


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:11', position='1,1,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:12', position='31,11,0')
    ap1 = net.addAccessPoint('ap1', wlans=2, ssid='ssid1,', position='10,10,0')
    ap2 = net.addAccessPoint('ap2', wlans=2, ssid='ssid2,', position='30,10,0')
    ap3 = net.addAccessPoint('ap3', wlans=2, ssid='ssid3,', position='50,10,0')
    c0 = net.addController('c0')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating Stations\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap2)
    net.addLink(ap1, intf='ap1-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap2, intf='ap2-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap3, intf='ap3-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])

    ap1.cmd('iw dev %s-mp1 interface add %s-mon0 type monitor' %
                 (ap1.name, ap1.name))
    ap2.cmd('iw dev %s-mp1 interface add %s-mon0 type monitor' %
                 (ap2.name, ap2.name))
    ap1.cmd('ifconfig %s-mon0 up' % ap1.name)
    ap2.cmd('ifconfig %s-mon0 up' % ap2.name)

    ifname='enp2s0'
    collector = environ.get('COLLECTOR','127.0.0.1')
    sampling = environ.get('SAMPLING','10')
    polling = environ.get('POLLING','10')
    sflow = 'ovs-vsctl -- --id=@sflow create sflow agent=%s target=%s ' \
            'sampling=%s polling=%s --' % (ifname,collector,sampling,polling)

    for ap in net.aps:
        sflow += ' -- set bridge %s sflow=@sflow' % ap
        print ' '.join([ap.name for ap in net.aps])
        quietRun(sflow)

    agent = '127.0.0.1'
    topo = {'nodes':{}, 'links':{}}
    for ap in net.aps:
        topo['nodes'][ap.name] = {'agent':agent, 'ports':{}}

    path = '/sys/devices/virtual/mac80211_hwsim/'
    for child in listdir(path):
        dir_ = '/sys/devices/virtual/mac80211_hwsim/'+'%s' % child+'/net/'
        for child_ in listdir(dir_):
            node = child_[:3]
            if node in topo['nodes']:
                ifindex = open(dir_+child_+'/ifindex').read().split('\n',1)[0]
                topo['nodes'][node]['ports'][child_] = {'ifindex': ifindex}

    path = '/sys/devices/virtual/net/'
    for child in listdir(path):
        parts = re.match('(^.+)-(.+)', child)
        if parts == None: continue
        if parts.group(1) in topo['nodes']:
            ifindex = open(path+child+'/ifindex').read().split('\n',1)[0]
            topo['nodes'][parts.group(1)]['ports'][child] = {'ifindex': ifindex}

    i = 0
    for ap1 in net.aps:
        j = 0
        for ap2 in net.aps:
            if j > i:
                linkName = '%s-%s' % (ap1.name, ap2.name)
                topo['links'][linkName] = {'node1': ap1.name, 'port1': 'ap1-mp1',
                                           'node2': ap2.name, 'port2': 'ap2-mp1'}
                #topo['links'][linkName] = {'node1': ap1.name, 'port1': 'ap1-mon0',
                                          # 'node2': ap2.name, 'port2': 'ap2-mon0'}

                intfs = ap1.connectionsTo(ap2)
                for intf in intfs:
                    #ap1ifIdx = topo['nodes'][ap1.name]['ports'][intf[0].name]['ifindex']
                    #ap2ifIdx = topo['nodes'][ap2.name]['ports'][intf[1].name]['ifindex']
                    linkName = '%s-%s' % (ap1.name, ap2.name)
                    topo['links'][linkName] = {'node1': ap1.name, 'port1': intf[0].name,
                                               'node2': ap2.name, 'port2': intf[1].name}
            j += 1
        i += 1

    put('http://127.0.0.1:8008/topology/json',data=dumps(topo))

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
