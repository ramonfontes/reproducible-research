#!/usr/bin/python

# autor: Ramon dos Reis Fontes
# sflow-based code

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from json import dumps
from requests import put
from mininet.util import quietRun
from os import listdir, environ
import re


def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:11', position='1,1,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:12', position='31,11,0')
    ap1 = net.addAccessPoint('ap1', wlans=2, ssid=['ssid1','mesh'], position='10,10,0')
    ap2 = net.addAccessPoint('ap2', wlans=2, ssid=['ssid2','mesh'], position='30,10,0')
    ap3 = net.addAccessPoint('ap3', wlans=2, ssid=['ssid3','mesh'], position='50,10,0')
    c0 = net.addController('c0')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating Stations\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap2)

    info("*** Creating mesh links\n")
    net.addLink(ap1, intf='ap1-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap2, intf='ap2-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap3, intf='ap3-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)

    info("*** Building network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])

    ap1.cmd('iw dev %s-mp2 interface add %s-mon0 type monitor' %
                 (ap1.name, ap1.name))
    ap2.cmd('iw dev %s-mp2 interface add %s-mon0 type monitor' %
                 (ap2.name, ap2.name))
    ap1.cmd('ifconfig %s-mon0 up' % ap1.name)
    ap2.cmd('ifconfig %s-mon0 up' % ap2.name)

    ifname='enp2s0'  # have to be changed to your own iface!
    collector = environ.get('COLLECTOR','127.0.0.1')
    sampling = environ.get('SAMPLING','10')
    polling = environ.get('POLLING','10')
    sflow = 'ovs-vsctl -- --id=@sflow create sflow agent=%s target=%s ' \
            'sampling=%s polling=%s --' % (ifname,collector,sampling,polling)

    for ap in net.aps:
        sflow += ' -- set bridge %s sflow=@sflow' % ap
        info(' '.join([ap.name for ap in net.aps]))
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
        if parts is None: continue
        if parts.group(1) in topo['nodes']:
            ifindex = open(path+child+'/ifindex').read().split('\n',1)[0]
            topo['nodes'][parts.group(1)]['ports'][child] = {'ifindex': ifindex}

    linkName = '%s-%s' % (ap1.name, ap2.name)
    topo['links'][linkName] = {'node1': ap1.name, 'port1': 'ap1-mp2',
                               'node2': ap2.name, 'port2': 'ap2-mp2'}
    linkName = '%s-%s' % (ap2.name, ap3.name)
    topo['links'][linkName] = {'node1': ap2.name, 'port1': 'ap2-mp2',
                               'node2': ap3.name, 'port2': 'ap3-mp2'}
    linkName = '%s-%s' % (ap1.name, ap2.name)
    topo['links'][linkName] = {'node1': ap1.name, 'port1': ap1.wintfs[0].name,
                               'node2': ap2.name, 'port2': ap2.wintfs[0].name}

    put('http://127.0.0.1:8008/topology/json',data=dumps(topo))

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
