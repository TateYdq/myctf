import sys
#pip install python-nmap
from scapy.all import *

def scapyArpFunc(dst):
    ans,unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=dst),timeout=2)
    for snd,rcv in ans:
        print(rcv.sprintf("%Ether.src% - %ARP.psrc% is alive"))


def main():
    if len(sys.argv)!= 2:
        print("Usage:scanHost <IP>\n eg.python arpPing.py 192.168.1.1")
        sys.exit(1)
    dst = sys.argv[1]
    scapyArpFunc(dst)

if __name__ == '__main__':
    main()