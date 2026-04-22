import sys
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info, error
import time
import os

def create_network():
    info("\n[*] Creating network topology...\n")
    
    net = Mininet(
        controller=RemoteController,
        switch=OVSSwitch,
        link=TCLink
    )
    
    c0 = net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6633
    )
    
    s1 = net.addSwitch('s1')
    
    h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
    h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
    h4 = net.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04')
    
    net.addLink(s1, h1, delay='1ms')
    net.addLink(s1, h2, delay='1ms')
    net.addLink(s1, h3, delay='1ms')
    net.addLink(s1, h4, delay='1ms')
    
    info("[+] Network topology created\n")
    info("    Switch: s1\n")
    info("    Hosts: h1 (10.0.0.1), h2 (10.0.0.2), h3 (10.0.0.3), h4 (10.0.0.4)\n")
    
    return net

def start_network(net):
    info("\n[*] Starting network...\n")
    net.start()
    time.sleep(2)
    info("[+] Network started successfully!\n")

def test_connectivity(net):
    info("\n[*] Testing connectivity...\n")
    h1 = net.get('h1')
    h2 = net.get('h2')
    
    result = h1.cmd('ping -c 1 10.0.0.2')
    if '1 received' in result:
        info("[+] Connectivity test PASSED\n")
    else:
        error("[-] Connectivity test FAILED\n")

def cleanup():
    info("[*] Cleaning up network...\n")
    os.system('sudo mn -c')

def main():
    setLogLevel('info')
    
    if os.getuid() != 0:
        error("\n[ERROR] This script must be run with sudo!\n")
        error("Usage: sudo python3 topology.py\n")
        sys.exit(1)
    
    try:
        net = create_network()
        start_network(net)
        test_connectivity(net)
        
        info("\n" + "="*70 + "\n")
        info("Network is running. Test traffic classification:\n")
        info("  ICMP (ping): h1 ping -c 5 10.0.0.2\n")
        info("  TCP:        h1 nc -w 1 10.0.0.2 5000\n")
        info("  UDP:        h1 nc -u -w 1 10.0.0.3 5000\n")
        info("  Exit:       exit\n")
        info("\nWatch Terminal 1 for traffic classification output.\n")
        info("="*70 + "\n")
        
        CLI(net)
    except KeyboardInterrupt:
        info("\n[*] Interrupted by user\n")
    finally:
        info("\n[*] Stopping network...\n")
        net.stop()
        cleanup()

if __name__ == '__main__':
    main()
