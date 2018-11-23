#!/usr/bin/python

"""This code illustrates a single case about Vehicular Ad-Hoc Networks.
More detail about VANET implementation can be found at the paper titled
From Theory to Experimental Evaluation: Resource Management
in Software-Defined Vehicular Networks
url: http://ieeexplore.ieee.org/document/7859348/
Video clip available at: https://www.youtube.com/watch?v=kO3O9EwrP_s
"""

import os
import time
import matplotlib.pyplot as plt

from mininet.log import setLogLevel, info
from mininet.node import Controller
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI_wifi
from mn_wifi.wmediumdConnector import interference
from mn_wifi.link import wmediumd, mesh


s1_pkt = 's1-pkt.vanetdata'
s1_throughput = 's1-throughput.vanetdata'
c0_pkt = 'c0-pkt.vanetdata'
c0_throughput = 'c0-throughput.vanetdata'


def graphic():

    f1 = open('./' + s1_pkt, 'r')
    s_pkt = f1.readlines()
    f1.close()

    f11 = open('./' + s1_throughput, 'r')
    s_throughput = f11.readlines()
    f11.close()

    f2 = open('./' + c0_pkt, 'r')
    c_pkt = f2.readlines()
    f2.close()

    f21 = open('./' + c0_throughput, 'r')
    c_throughput = f21.readlines()
    f21.close()

    # initialize some variable to be lists:
    time_ = []

    l1 = []
    l2 = []
    t1 = []
    t2 = []

    ll1 = []
    ll2 = []
    tt1 = []
    tt2 = []

    # scan the rows of the file stored in lines, and put the values into some variables:
    i = 0
    for x in s_pkt:
        p = x.split()
        l1.append(int(p[0]))
        if len(l1) > 1:
            ll1.append(l1[i] - l1[i - 1])
        i += 1

    i = 0
    for x in s_throughput:
        p = x.split()
        t1.append(int(p[0]))
        if len(t1) > 1:
            tt1.append(t1[i] - t1[i - 1])
        i += 1

    i = 0
    for x in c_pkt:
        p = x.split()
        l2.append(int(p[0]))
        if len(l2) > 1:
            ll2.append(l2[i] - l2[i - 1])
        i += 1

    i = 0
    for x in c_throughput:
        p = x.split()
        t2.append(int(p[0]))
        if len(t2) > 1:
            tt2.append(t2[i] - t2[i - 1])
        i += 1

    i = 0
    for x in range(len(ll1)):
        time_.append(i)
        i = i + 0.5

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.plot(time_, ll1, color='red', label='Received Data (client)',
             markevery=7, linewidth=1)
    ax1.plot(time_, ll2, color='black', label='Transmited Data (server)',
             markevery=7, linewidth=1)
    ax2.plot(time_, tt1, color='red', label='Throughput (client)', ls="--",
             markevery=7, linewidth=1)
    ax2.plot(time_, tt2, color='black', label='Throughput (server)', ls='--',
             markevery=7, linewidth=1)
    ax1.legend(loc=2, borderaxespad=0., fontsize=12)
    ax2.legend(loc=1, borderaxespad=0., fontsize=12)

    ax2.set_yscale('log')

    ax1.set_ylabel("# Packets (unit)", fontsize=18)
    ax1.set_xlabel("Time (seconds)", fontsize=18)
    ax2.set_ylabel("Throughput (bytes/sec)", fontsize=18)

    plt.show()
    plt.savefig("graphic.eps")


def recordValues(car, client, kernel):
    if kernel == 1:
        car.cmd('ifconfig bond0 | grep \"TX packets\" | awk -F\' \' \'{print $3}\' >> %s' % c0_pkt)
        client.cmd('ifconfig client-eth0 | grep \"RX packets\" | awk -F\' \' \'{print $3}\' >> %s' % s1_pkt)
        car.cmd('ifconfig bond0 | grep \"bytes\" | awk -F\' \' \'NR==2{print $5}\' >> %s' % c0_throughput)
        client.cmd('ifconfig client-eth0 | grep \"bytes\" | awk -F\' \' \'NR==1{print $5}\' >> %s' % s1_throughput)
    else:
        car.cmd('ifconfig bond0 | grep \"TX packets\" | awk -F\' \' \'{print $2}\' | tr -d packets: >> %s' % c0_pkt)
        client.cmd('ifconfig client-eth0 | grep \"RX packets\" | awk -F\' \' \'{print $2}\' | tr -d packets: >> %s' % s1_pkt)
        car.cmd('ifconfig bond0 | grep \"bytes\" | awk -F\' \' \'NR==1{print $6}\' | tr -d bytes: >> %s' % c0_throughput)
        client.cmd('ifconfig client-eth0 | grep \"bytes\" | awk -F\' \' \'NR==1{print $2}\' | tr -d \'RX bytes:\' >> %s' % s1_throughput)


def topology():

    taskTime = 20
    ncars = 4

    "Create a network."
    net = Mininet_wifi(controller=Controller, autoAssociation=True,
                       link=wmediumd,
                       wmediumd_mode=interference)

    info("*** Creating nodes\n")
    cars = []
    for idx in range(1, ncars+1):
        cars.append(net.addCar('car%s' % idx,
                               wlans=2,
                               ip='10.0.0.%s/8'% (idx + 1),
                               range="50,50",
                               mac='00:00:00:00:00:0%s' % idx,
                               mode='b',
                               position='%d,%d,0'
                                        % ((120 - (idx * 20)),
                                           (100 - (idx * 0)))))

    enb1 = net.addStation('enb1', position='80,75,0')
    enb2 = net.addStation('enb2', position='180,75,0')
    rsu1 = net.addStation('rsu1', position='140,120,0')
    client = net.addHost ('client', ip='192.168.10.1/24')
    r1 = net.addHost('r1')
    s1 = net.addSwitch ('s1')
    c0 = net.addController('c0')

    client.plot(position='125,230,0')
    r1.plot(position='125,210,0')
    s1.plot(position='125,200,0')

    info("*** Setting bgscan\n")
    net.setBgscan(signal=-60, s_inverval=2, l_interval=5)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3.5)

    net.addMacToWmediumd({cars[0]:['02:01:02:03:04:08','bond0']})

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    enb1.setMasterMode(intf='enb1-wlan0', ssid='slice-ssid',
                       channel='36', mode='ac',
                       passwd='123456789a', encrypt='wpa2')
    enb2.setMasterMode(intf='enb2-wlan0', ssid='slice-ssid',
                       channel='40', mode='ac',
                       passwd='123456789a', encrypt='wpa2')
    rsu1.setMasterMode(intf='rsu1-wlan0', ssid='slice-ssid',
                       channel='11', mode='g',
                       passwd='123456789a', encrypt='wpa2')

    info("*** Creating links\n")
    net.addLink(enb1, s1)
    net.addLink(enb2, s1)
    net.addLink(rsu1, s1)
    net.addLink(enb1, cars[0], wifi='enb1')
    net.addLink(enb1, cars[1], wifi='enb1')
    net.addLink(enb1, cars[2], wifi='enb1')
    net.addLink(enb1, cars[3], wifi='enb1')
    net.addLink(s1, r1)
    net.addLink(r1, client)

    for car in cars:
        net.addLink(car, intf=car.params['wlan'][1],
                    cls=mesh, ssid='mesh-ssid', channel=5,
                    passwd='thisisreallysecret')

    'Plotting Graph'
    net.plotGraph(max_x=300, max_y=300)

    info("*** Starting network\n")
    net.build()
    c0.start()
    s1.start([c0])

    #client.setIP('192.168.10.1/24', intf='client-eth0')
    r1.setIP('192.168.100.1/24', intf='r1-eth0')
    r1.setIP('192.168.10.254/24', intf='r1-eth1')
    enb1.setIP('192.168.100.2/24', intf='enb1-eth2')
    enb2.setIP('192.168.100.3/24', intf='enb2-eth2')
    rsu1.setIP('192.168.100.4/24', intf='rsu1-eth2')
    enb1.setIP('192.168.200.101/24', intf='enb1-wlan0')
    enb2.setIP('192.168.200.102/24', intf='enb2-wlan0')
    rsu1.setIP('192.168.200.103/24', intf='rsu1-wlan0')

    for car in cars:
        car.setIP('192.168.200.%s/24' % (int(cars.index(car))+1),
                  intf='%s-wlan0' % car)
        car.setIP('10.0.0.%s/24' % (int(cars.index(car))+1),
                  intf='%s-mp1' % car)

    cars[0].setPosition('100,100,0')
    cars[1].setPosition('80,100,0')
    cars[2].setPosition('60,100,0')
    cars[3].setPosition('40,100,0')

    cars[0].cmd('modprobe bonding mode=3')
    cars[0].cmd('ip link add bond0 type bond')
    cars[0].cmd('ip link set bond0 address 02:01:02:03:04:08')
    cars[0].cmd('ip link set car1-wlan0 down')
    cars[0].cmd('ip link set car1-wlan0 address 00:00:00:00:00:15')
    cars[0].cmd('ip link set car1-wlan0 master bond0')
    cars[0].cmd('ip link set car1-mp1 down')
    cars[0].cmd('ip link set car1-mp1 address 00:00:00:00:00:16')
    cars[0].cmd('ip link set car1-mp1 master bond0')
    cars[0].cmd('ip addr add 192.168.200.1/24 dev bond0')
    cars[0].cmd('ip link set bond0 up')
    cars[0].cmd('ifconfig car1-mp1 0')
    cars[0].cmd('ifconfig bond0:0 10.0.0.1')

    r1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    enb1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    enb2.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    rsu1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')

    client.cmd('route add default gw 192.168.10.254')
    cars[0].cmd('route add default gw 192.168.200.101')
    cars[1].cmd('route add default gw 192.168.200.101')
    cars[2].cmd('route add default gw 192.168.200.101')
    cars[3].cmd('route add default gw 192.168.200.101')
    enb1.cmd('ip route add to 192.168.10.1 via 192.168.100.1')
    r1.cmd('ip route add to 192.168.200.1 via 192.168.100.2')
    r1.cmd('ip route add to 192.168.200.2 via 192.168.100.2')
    r1.cmd('ip route add to 192.168.200.3 via 192.168.100.2')
    r1.cmd('ip route add to 192.168.200.4 via 192.168.100.2')

    os.system('rm *.vanetdata')

    #os.system('xterm -hold -title "car0" -e "util/m car0 ping 200.0.10.2" &')
    cars[0].cmdPrint("cvlc -vvv v4l2:///dev/video0 --mtu 1000 --sout \'#transcode{vcodec=mp4v,vb=800,scale=1,\
                acodec=mpga,ab=128,channels=1}: duplicate{dst=display,dst=rtp{sdp=rtsp://192.168.200.1:8080/helmet.sdp}}\' &")
    client.cmdPrint("cvlc rtsp://192.168.200.1:8080/helmet.sdp &")

    os.system('ovs-ofctl mod-flows s1 in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows s1 in_port=2,actions=drop')
    os.system('ovs-ofctl mod-flows s1 in_port=3,actions=drop')

    time.sleep(2)

    print("applying first rule")
    os.system('ovs-ofctl mod-flows s1 in_port=1,actions=output:4')
    os.system('ovs-ofctl mod-flows s1 in_port=4,actions=output:1')
    os.system('ovs-ofctl mod-flows s1 in_port=2,actions=drop')
    os.system('ovs-ofctl mod-flows s1 in_port=3,actions=drop')

    cars[0].cmd('route del default gw 192.168.200.101')
    cars[1].cmd('route del default gw 192.168.200.101')
    cars[0].cmd('route add default gw 192.168.200.103')
    cars[1].cmd('route add default gw 192.168.200.103')

    r1.cmd('ip route del to 192.168.200.1 via 192.168.100.2')
    r1.cmd('ip route del to 192.168.200.2 via 192.168.100.2')
    r1.cmd('ip route add to 192.168.200.1 via 192.168.100.4')
    r1.cmd('ip route add to 192.168.200.2 via 192.168.100.4')

    kernel = 0
    var = client.cmd('ifconfig client-eth0 | grep \"bytes\" | awk -F\' \' \'NR==1{print $5}\'')
    if var:
        kernel = 1

    timeout = time.time() + taskTime
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break
        if time.time() - currentTime >= i:
            recordValues(cars[0], client, kernel)
            i += 0.5

    info("Moving nodes\n")
    cars[0].setPosition('150,100,0')
    cars[1].setPosition('120,100,0')
    cars[2].setPosition('90,100,0')
    cars[3].setPosition('70,100,0')

    # time.sleep(3)

    info("applying second rule\n")
    os.system('ovs-ofctl mod-flows s1 in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows s1 in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows s1 in_port=4,actions=output:2,3')
    os.system('ovs-ofctl mod-flows s1 in_port=3,actions=output:4')

    cars[0].cmd('route del default gw 192.168.200.103')
    cars[0].cmd('route add default gw 192.168.200.102')
    cars[1].cmd('route add default gw 192.168.200.103')
    cars[2].cmd('route del default gw 192.168.200.101')
    cars[2].cmd('route add default gw 192.168.200.103')

    r1.cmd('ip route del to 192.168.200.3 via 192.168.100.2')
    r1.cmd('ip route del to 192.168.200.1 via 192.168.100.4')
    r1.cmd('ip route del to 192.168.200.2 via 192.168.100.4')
    r1.cmd('ip route add to 192.168.200.1 via 192.168.100.3')
    r1.cmd('ip route add to 192.168.200.2 via 192.168.100.3')
    r1.cmd('ip route add to 192.168.200.3 via 192.168.100.4')

    timeout = time.time() + taskTime
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break
        if time.time() - currentTime >= i:
            recordValues(cars[0], client, kernel)
            i += 0.5

    info("Moving nodes\n")
    cars[0].setPosition('170,100,0')
    cars[1].setPosition('150,100,0')
    cars[2].setPosition('120,100,0')
    cars[3].setPosition('90,100,0')

    # time.sleep(2)

    info("applying third rule\n")
    os.system('ovs-ofctl mod-flows s1 in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows s1 in_port=3,actions=drop')
    os.system('ovs-ofctl mod-flows s1 in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows s1 in_port=4,actions=output:2')
    timeout = time.time() + taskTime
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break
        if time.time() - currentTime >= i:
            recordValues(cars[0], client, kernel)
            i += 0.5

    info("*** Generating graph\n")
    graphic()

    os.system('pkill -f vlc')
    os.system('pkill xterm')

    info("*** Running CLI\n")
    CLI_wifi(net)

    #os.system('rm *.vanetdata')

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
