# CN-SDN: Traffic Classification System

A Software Defined Networking (SDN) project that classifies network traffic using POX controller and Mininet.

## Project Overview
This project implements a Traffic Classification System that:
- Identifies TCP, UDP, and ICMP packets
- Maintains per-protocol statistics
- Displays real-time traffic distribution percentages

## Files
- `traffic_classifier.py` — POX SDN controller that classifies network traffic
- `topology.py` — Mininet network topology with 1 switch and 4 hosts

## Requirements
- Python 3
- POX Controller
- Mininet
- OpenvSwitch

## Setup and Usage

### Terminal 1 — Start POX Controller:
```bash
cd ~/Desktop/pox
python3 pox.py forwarding.traffic_classifier
```

### Terminal 2 — Start Mininet Topology:
```bash
sudo python3 topology.py
```

### Generate Traffic (inside Mininet CLI):
```bash
# ICMP traffic
h1 ping -c 5 10.0.0.2

# TCP traffic
h2 iperf -s &
h1 iperf -c 10.0.0.2 -t 2

# UDP traffic
h2 iperf -s -u &
h1 iperf -c 10.0.0.2 -u -t 2
```
## Network Topology
- 1 OpenFlow Switch (s1)
- 4 Hosts: h1 (10.0.0.1), h2 (10.0.0.2), h3 (10.0.0.3), h4 (10.0.0.4)
- Remote Controller on 127.0.0.1:6633
