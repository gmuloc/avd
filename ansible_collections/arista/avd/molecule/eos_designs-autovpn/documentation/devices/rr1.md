# rr1

## Table of Contents

- [Management](#management)
  - [Management API HTTP](#management-api-http)
- [Spanning Tree](#spanning-tree)
  - [Spanning Tree Summary](#spanning-tree-summary)
  - [Spanning Tree Device Configuration](#spanning-tree-device-configuration)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
  - [Internal VLAN Allocation Policy Configuration](#internal-vlan-allocation-policy-configuration)
- [IP Security](#ip-security)
  - [IKE policies](#ike-policies)
  - [IPSec profiles](#ipsec-profiles)
  - [IP Security Configuration](#ip-security-configuration)
- [Interfaces](#interfaces)
  - [Ethernet Interfaces](#ethernet-interfaces)
  - [Loopback Interfaces](#loopback-interfaces)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [Router BGP](#router-bgp)
- [BFD](#bfd)
  - [Router BFD](#router-bfd)
- [VRF Instances](#vrf-instances)
  - [VRF Instances Summary](#vrf-instances-summary)
  - [VRF Instances Device Configuration](#vrf-instances-device-configuration)
  - [Router Path-selection](#router-path-selection)
- [STUN](#stun)
  - [STUN Server](#stun-server)
  - [STUN Device Configuration](#stun-device-configuration)

## Management

### Management API HTTP

#### Management API HTTP Summary

| HTTP | HTTPS | Default Services |
| ---- | ----- | ---------------- |
| False | True | - |

#### Management API VRF Access

| VRF Name | IPv4 ACL | IPv6 ACL |
| -------- | -------- | -------- |
| MGMT | - | - |

#### Management API HTTP Configuration

```eos
!
management api http-commands
   protocol https
   no shutdown
   !
   vrf MGMT
      no shutdown
```

## Spanning Tree

### Spanning Tree Summary

STP mode: **none**

### Spanning Tree Device Configuration

```eos
!
spanning-tree mode none
```

## Internal VLAN Allocation Policy

### Internal VLAN Allocation Policy Summary

| Policy Allocation | Range Beginning | Range Ending |
| ------------------| --------------- | ------------ |
| ascending | 1006 | 1199 |

### Internal VLAN Allocation Policy Configuration

```eos
!
vlan internal order ascending range 1006 1199
```

## IP Security

### IKE policies

| Policy name | Local ID |
| ----------- | -------- |
| IKEAUTOVPN | 192.168.42.1 |

### IPSec profiles

| Profile name | IKE policy | SA policy | Connection | DPD Interval | DPD Time | DPD action | Mode |
| ------------ | ---------- | ----------| ---------- | ------------ | -------- | ---------- | ---- |
| AUTOVPNTUNNEL | IKEAUTOVPN | SAAUTOVPN | start | - | - | - | transport |

### IP Security Configuration

```eos
!
ip security
   !
   ike policy IKEAUTOVPN
      local-id 192.168.42.1
   !
   sa policy SAAUTOVPN
   !
   profile AUTOVPNTUNNEL
      ike-policy IKEAUTOVPN
      sa-policy SAAUTOVPN
      connection start
      shared-key 7 0112140D481F07
      dpd 10 50 clear
      mode transport
```

## Interfaces

### Ethernet Interfaces

#### Ethernet Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Type | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | -----| ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | WAN_MPLS-1 | routed | - | dhcp | default | - | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description WAN_MPLS-1
   no shutdown
   no switchport
   ip address dhcp
   dhcp client accept default-route
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | EVPN_Overlay_Peering | default | 192.168.42.1/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | EVPN_Overlay_Peering | default | - |


#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description EVPN_Overlay_Peering
   no shutdown
   ip address 192.168.42.1/32
```

## Routing

### Service Routing Protocols Model

Multi agent routing protocol model enabled

```eos
!
service routing protocols model multi-agent
```

### IP Routing

#### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | True |
| MGMT | False |

#### IP Routing Device Configuration

```eos
!
ip routing
no ip routing vrf MGMT
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| MGMT | false |

### Router BGP

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65000 | 192.168.42.1 |

| BGP AS | Cluster ID |
| ------ | --------- |
| 65000 | 192.168.42.1 |

| BGP Tuning |
| ---------- |
| update wait-install |
| no bgp default ipv4-unicast |
| maximum-paths 4 ecmp 4 |

#### Router BGP Listen Ranges

| Prefix | Peer-ID Include Router ID | Peer Group | Peer-Filter | Remote-AS | VRF |
| ------ | ------------------------- | ---------- | ----------- | --------- | --- |

#### Router BGP Peer Groups

##### autovpnEdges

| Settings | Value |
| -------- | ----- |
| Address Family | wan |
| Remote AS | 65000 |
| Route Reflector Client | Yes |
| Source | Loopback0 |
| Send community | all |
| Maximum routes | 12000 |

#### Router BGP EVPN Address Family

##### EVPN Peer Groups

| Peer Group | Activate | Encapsulation |
| ---------- | -------- | ------------- |
| autovpnEdges | True | default |

#### Router BGP Path-Selection Address Family

##### Path-Selection Peer Groups

| Peer Group | Activate |
| ---------- | -------- |
| autovpnEdges | True |

#### Router BGP Device Configuration

```eos
!
router bgp 65000
   router-id 192.168.42.1
   maximum-paths 4 ecmp 4
   update wait-install
   no bgp default ipv4-unicast
   bgp cluster-id 192.168.42.1
   neighbor autovpnEdges peer group
   neighbor autovpnEdges remote-as 65000
   neighbor autovpnEdges update-source Loopback0
   neighbor autovpnEdges route-reflector-client
   neighbor autovpnEdges password 7 <removed>
   neighbor autovpnEdges send-community
   neighbor autovpnEdges maximum-routes 12000
   !
   address-family evpn
      neighbor autovpnEdges activate
   !
   address-family ipv4
      no neighbor autovpnEdges activate
      no neighbor EVPN-OVERLAY-PEERS activate
   !
   address-family path-selection
      bgp additional-paths receive
      bgp additional-paths send any
      neighbor autovpnEdges activate
      neighbor autovpnEdges additional-paths receive
      neighbor autovpnEdges additional-paths send any
```

## BFD

### Router BFD

#### Router BFD Multihop Summary

| Interval | Minimum RX | Multiplier |
| -------- | ---------- | ---------- |
| 300 | 300 | 3 |

#### Router BFD Device Configuration

```eos
!
router bfd
   multihop interval 300 min-rx 300 multiplier 3
```

## VRF Instances

### VRF Instances Summary

| VRF Name | IP Routing |
| -------- | ---------- |
| MGMT | disabled |

### VRF Instances Device Configuration

```eos
!
vrf instance MGMT
```

### Router Path-selection

#### Router Path-selection Summary

| Setting | Value |
| ------  | ----- |
| Dynamic peers source | STUN |

#### Path Groups

##### Path Group MPLS-1

| Setting | Value |
| ------  | ----- |
| Path Group ID | 100 |
| IPSec profile | AUTOVPNTUNNEL |

###### Local Interfaces

| Interface name | Public address | STUN server profile(s) |
| -------------- | -------------- | ---------------------- |
| Ethernet1 | - |  |

#### Load-balance policies

| Policy name | Path group(s) |
| ----------- | ------------- |
| LBPOLICY | MPLS-1 |

#### DPS policies

##### DPS policy dps-policy-default

| Rule ID | Application profile | Load-balance policy |
| ------- | ------------------- | ------------------- |
| Default Match | - | LBPOLICY |

#### VRFs configuration

| VRF name | DPS policy |
| -------- | ---------- |
| default | dps-policy-default |

#### Router Path-selection Device Configuration

```eos
!
router path-selection
   peer dynamic source stun
   !
   path-group MPLS-1 id 100
      ipsec profile AUTOVPNTUNNEL
      !
      local interface Ethernet1
   !
   load-balance policy LBPOLICY
      path-group MPLS-1
   !
   policy dps-policy-default
      default-match
         load-balance LBPOLICY
   !
   vrf default
      path-selection-policy dps-policy-default
```

## STUN

### STUN Server

| Server local interfaces |
| ----------------------- |
| Ethernet1 |

### STUN Device Configuration

```eos
!
stun
   server
      local-interface Ethernet1
```
