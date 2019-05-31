#!/usr/bin/python

from scapy.all import *
import os


NODE_ID = 1
CLIENT = '02:00:00:00:00:%02d' % NODE_ID
MININET_WIFI_DIR = '~/mininet-wifi/util/m'

rssi = 0
t = 0

def pkt_callback(pkt):
    global t
    t += 1
    if t >= 201:
        if pkt.haslayer(Dot11):
            ssid = None
            try:
                extra = pkt.notdecoded
                _rssi = -(256 - ord(extra[-4:-3]))
            except:
                _rssi = None

            if pkt.type == 0 and pkt.subtype == 8:
                ssid = pkt.info

            cmd = ["%s car%s iw dev "
                   "car%s-wlan0 link | grep Connected | "
                   "awk 'NR==1{print $3}'" % (MININET_WIFI_DIR, NODE_ID, NODE_ID)]
            address = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (out, err) = address.communicate()
            bssid = str(out).split('\n')[0]
            if str(pkt.addr1) == "ff:ff:ff:ff:ff:ff":
                global rssi
                target_bssid = ''
                target_signal = -100
                target_n_clients = 0
                if bssid != pkt.addr2:
                    target_bssid = pkt.addr2
                    target_signal = _rssi
                    ap_id = "%01d" % (int(target_bssid[-2:]),)
                    target_n_clients = \
                        int(subprocess.check_output('%s enb%s '
                                                    'hostapd_cli -i enb%s-wlan1 '
                                                    'list_sta | wc -l'
                                                    % (MININET_WIFI_DIR, ap_id, ap_id),
                                                    shell=True))
                else:
                    rssi = _rssi

                if bssid:
                    bssid_id = "%01d" % (int(bssid[-2:]),)
                    n_clients = \
                        int(subprocess.check_output('%s enb%s '
                                                    'hostapd_cli -i enb%s-wlan1 '
                                                    'list_sta | wc -l'
                                                    % (MININET_WIFI_DIR, bssid_id, bssid_id),
                                                    shell=True))

                    if target_bssid:
                        msg = "%s,%s,%s,%s,%s,%s,%s,%s" % (
                            CLIENT,bssid,ssid,rssi,target_bssid,
                            target_signal,n_clients,target_n_clients)
                        packet = IP(src="10.0.0.%s" % NODE_ID,
                                    dst="172.17.0.%d"
                                        % (int(bssid_id)+1))/UDP(sport=8000, dport=8002)/msg
                        send(packet, verbose=0, iface="car%s-wlan0" % NODE_ID)
                        t = 0


sniff(iface="car%s-mon0" % NODE_ID, prn=pkt_callback, store=0)
