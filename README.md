# SDN Learning Switch using POX & Mininet

## 🔹 Problem Statement

Implement a Software Defined Network (SDN) learning switch using POX controller and Mininet. The switch should dynamically learn MAC addresses and install flow rules to optimize packet forwarding.

---

## 🔹 Objective

* Understand SDN architecture
* Implement MAC learning switch logic
* Observe PacketIn and flow rule installation
* Analyze network performance

---

## 🔹 Topology

* 2 Hosts (h1, h2)
* 1 Switch (s1)
* 1 Controller (POX)

---

## 🔹 Setup Instructions

### Step 1: Start POX Controller

```bash
cd ~/Desktop/pox
./pox.py log.level --DEBUG forwarding.l2_learning info.packet_dump
```

### Step 2: Start Mininet

```bash
sudo mn --topo single,2 --controller remote --switch ovsk
```

### Step 3: Test Connectivity

```bash
pingall
```

---

## 🔹 Expected Output

* First packet triggers controller:

  * PacketIn event (seen as packet_dump logs)
  * Flooding occurs
* Controller learns MAC addresses
* Flow rules are installed:

```
installing flow for MAC → MAC
```

* Subsequent packets bypass controller

---

## 🔹 Observations

* Initial latency is higher due to controller involvement
* After flow installation, latency reduces
* Switch forwards packets directly

---

## 🔹 Proof of Execution

### ✔ Ping Results

* 0% packet loss

### ✔ Controller Logs

* Packet dump logs visible
* Flow installation messages observed

### ✔ Flow Table (Optional Command)

```bash
sudo ovs-ofctl dump-flows s1
```

---

## 🔹 Conclusion

The SDN learning switch successfully learns MAC addresses and installs flow rules, reducing controller dependency and improving efficiency.

---

## 🔹 References

* POX Documentation
* Mininet Documentation
* OpenFlow Specification
