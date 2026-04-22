from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ipv4 import ipv4

log = core.getLogger()

class TrafficClassifier(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)
        self.tcp_count = 0
        self.udp_count = 0
        self.icmp_count = 0

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            return

        if packet.find('arp'):
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
            return

        ip_packet = packet.find('ipv4')
        if ip_packet is None:
            return

        if packet.find('tcp'):
            self.tcp_count += 1
            log.info("TCP Packet | Count: %d" % self.tcp_count)

        elif packet.find('udp'):
            self.udp_count += 1
            log.info("UDP Packet | Count: %d" % self.udp_count)

        elif packet.find('icmp'):
            self.icmp_count += 1
            log.info("ICMP Packet | Count: %d" % self.icmp_count)

        total = self.tcp_count + self.udp_count + self.icmp_count
        if total > 0:
            tcp_per = (self.tcp_count / total) * 100
            udp_per = (self.udp_count / total) * 100
            icmp_per = (self.icmp_count / total) * 100
            print("\n===== TRAFFIC ANALYSIS =====")
            print("TCP:  %.2f%%" % tcp_per)
            print("UDP:  %.2f%%" % udp_per)
            print("ICMP: %.2f%%" % icmp_per)
            print("============================\n")

        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(msg)

def launch():
    def start_switch(event):
        log.debug("Controlling %s" % (event.connection,))
        TrafficClassifier(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
