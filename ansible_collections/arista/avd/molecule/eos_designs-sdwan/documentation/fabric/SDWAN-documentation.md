# SDWAN

## Table of Contents

- [Fabric Switches and Management IP](#fabric-switches-and-management-ip)
  - [Fabric Switches with inband Management IP](#fabric-switches-with-inband-management-ip)
- [Fabric Topology](#fabric-topology)
- [Fabric IP Allocation](#fabric-ip-allocation)
  - [Fabric Point-To-Point Links](#fabric-point-to-point-links)
  - [Point-To-Point Links Node Allocation](#point-to-point-links-node-allocation)
  - [Loopback Interfaces (BGP EVPN Peering)](#loopback-interfaces-bgp-evpn-peering)
  - [Loopback0 Interfaces Node Allocation](#loopback0-interfaces-node-allocation)
  - [VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)](#vtep-loopback-vxlan-tunnel-source-interfaces-vteps-only)
  - [VTEP Loopback Node allocation](#vtep-loopback-node-allocation)
  - [SDWAN](#sdwan)

## Fabric Switches and Management IP

| POD | Type | Node | Management IP | Platform | Provisioned in CloudVision | Serial Number |
| --- | ---- | ---- | ------------- | -------- | -------------------------- | ------------- |
| SDWAN | pathfinder | pf1 | - | cloud-eos | Provisioned | - |
| SDWAN | pathfinder | pf2 | - | cloud-eos | Provisioned | - |
| SDWAN | edge | wan1-site1 | - | cloud-eos | Provisioned | - |
| SDWAN | edge | wan1-site2 | - | cloud-eos | Provisioned | - |
| SDWAN | edge | wan1-site3 | - | cloud-eos | Provisioned | - |
| SDWAN | edge | wan2-site1 | - | cloud-eos | Provisioned | - |
| SDWAN | edge | wan2-site2 | - | cloud-eos | Provisioned | - |

> Provision status is based on Ansible inventory declaration and do not represent real status from CloudVision.

### Fabric Switches with inband Management IP

| POD | Type | Node | Management IP | Inband Interface |
| --- | ---- | ---- | ------------- | ---------------- |

## Fabric Topology

| Type | Node | Node Interface | Peer Type | Peer Node | Peer Interface |
| ---- | ---- | -------------- | --------- | ----------| -------------- |

## Fabric IP Allocation

### Fabric Point-To-Point Links

| Uplink IPv4 Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ---------------- | ------------------- | ------------------ | ------------------ |

### Point-To-Point Links Node Allocation

| Node | Node Interface | Node IP Address | Peer Node | Peer Interface | Peer IP Address |
| ---- | -------------- | --------------- | --------- | -------------- | --------------- |

### Loopback Interfaces (BGP EVPN Peering)

| Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------- | ------------------- | ------------------ | ------------------ |
| 192.168.42.0/24 | 256 | 7 | 2.74 % |

### Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| SDWAN | pf1 | 192.168.42.1/32 |
| SDWAN | pf2 | 192.168.42.2/32 |
| SDWAN | wan1-site1 | 192.168.42.3/32 |
| SDWAN | wan1-site2 | 192.168.42.5/32 |
| SDWAN | wan1-site3 | 192.168.42.7/32 |
| SDWAN | wan2-site1 | 192.168.42.4/32 |
| SDWAN | wan2-site2 | 192.168.42.6/32 |

### VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| --------------------- | ------------------- | ------------------ | ------------------ |

### VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |

### SDWAN

#### Summary

**TODO:** add table with summary of regions and zones?


#### Region US_West

Region id: 1


| Site | Site ID | Zone | Zone ID | HA |
| ---- | ------- | ---- | ------- | -- |
| pf1 | 1 | Zone59 | 59 | False |
| site1 | 101 | Zone1 | 1 | True |
| site2 | 102 | Zone2 | 2 | True |

#### Region US_East

Region id: 2


| Site | Site ID | Zone | Zone ID | HA |
| ---- | ------- | ---- | ------- | -- |
| pf2 | 2 | Zone2 | 42 | False |
| site3 | 103 | Zone1 | 1 | False |
