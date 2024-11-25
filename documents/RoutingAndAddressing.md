
# Networking

- Fundamentals
- Routing and Addressing
- Security
- Load Balancing
- Hybrid and Multicloud
- 

## Routing and Addressing

- Network Routing and Addressing
- Private Connection Options

### Routing & Addressing

- Project -> Network -> Region -> Subnet -> VM
- Subnet and IP address
- Google Cloud VPCs let me increase the IP address space of any subnets without any workload shutdown or downtime.
- a network with subnets that have different subnet masks.
- subnet masks define the range of ip addresses allocated to a subnet within a VPC
- CIDR notation
  - 192.168.1.0/24 has:
    - a network prefix of 24 bits.
    - the remaining 8 bits available for host address.
    - total of 256 iP addresses form 192.169.1.0 to 192.168.1.255
  - GCP preserves 4 ip addresses in each subnet:
    - network address: first ip in the range (192.168.1.0) for identifying the subnet.
    - broadcast address: last ip in the range (192.168.1.255) for broadcasting (a communication method where a single message is sent to all devices on a specific network or subnet).
    - two reserved addresses for internal use by GCP.
    - /24 -> 2^(32-24) -4 = 256 -4 = 252.
  - Subnets are used to organize and isolate resources.
  - Subnets must not overlapping in the same VPC.
  - Route is a set of instructions that defines the path packets should follow to each a specific destination.
    - Components:
      - Destination: specifies the IP range or a specific IP address.
      - Next Hop: the next device or gateway where packets should be forwarded.
        - Default internet gateway, VPN tunnel, Peered VPC, instance
      - Priority: Lower values indicate higher priority.
    - Types of Routes
      - Default route, custom routes, subnet routes
  - Routing Table
    - A collection of routes that a network device (router, VM or switch) uses to determine how to forward traffic.
    - Components:
      - Destination or Prefix
      - Next Hop
      - Priority
      - Interface
  - Routing table in GCP
    - routing tables are not manually created or visible as standalone entities
    - they are implicitly part of the VPC network configuration
      - regionally distributed: each region has its own routes for subnets in that region.
    - Types:
      - system-generated routes
      - custom routes
  - System generated default routes form VPC to Google APIs and services
  - A default route is used only if a route with a more specific destination does not apply to a packet.
  - To completely isolated a network, delete the default route:
a
a
a