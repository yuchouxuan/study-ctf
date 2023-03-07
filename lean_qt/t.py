import scapy
from scapy.all import *
from scapy.utils import PcapReader
from scapy.layers.http import HTTPRequest, HTTPResponse, HTTP
packets=rdpcap("z:/ctf/misc.pcapng")
httppaks = packets.getlayer(HTTP)
http = httppaks[0]
ret = []
req = []
for pkt in httppaks:
    if pkt.haslayer(HTTPRequest):
        ret.append(pkt)
    if pkt.haslayer(HTTPResponse):
        req.append(pkt)
        pkt.show()
