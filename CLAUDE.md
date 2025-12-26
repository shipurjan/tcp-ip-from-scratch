# Network Protocol Learning Repository - Implementation Prompt

I want to build a GitHub repository that teaches networking protocols by implementing them from scratch using Python (Scapy) and C for the lowest layers. The goal is to show EXACTLY what each protocol is - the actual bytes, headers, and data structures - not just conceptual explanations.

## Tech Stack

**Primary: Python + Scapy**

- Used for 90% of examples
- Packet manipulation, visualization, and capture
- Clear field-by-field packet construction
- Interactive experimentation

**C for foundational examples**
- Raw socket programming (the hard way)
- Manual byte packing and header construction
- Shows what abstractions are hiding
- 2-3 examples max, then transition to Python

## Repository Structure


```
packets-from-scratch/
│
├── README.md                          # Overview, setup, learning path
├── requirements.txt                   # Python dependencies (scapy, etc.)
├── setup/
│   ├── install.md                     # Setup instructions
│   └── permissions.md                 # Raw socket privileges on Linux/macOS
│
├── utils/

│   ├── packet_visualizer.py           # Hex dump + decoded headers
│   ├── capture.py                     # Packet capture wrapper
│   └── helpers.py                     # Common utilities
│

├── docs/
│   ├── what-is-a-protocol.md          # Protocols = agreed byte formats
│   ├── tcp-ip-vs-osi.md               # Why we use TCP/IP model (reality vs theory)
│   ├── reading-rfcs.md                # How to read protocol specs
│   └── wireshark-guide.md             # Capturing and analyzing traffic
│
└── examples/
    ├── 00-foundations/
    │   ├── raw_socket.c               # C: Send raw bytes over network
    │   ├── raw_socket_explained.md    # What each line does
    │   ├── same_in_python.py          # Same thing in Python sockets
    │   └── same_in_scapy.py           # Same thing in Scapy (the easy way)

    │

    ├── 01-link-layer/
    │   ├── ethernet_frame.py          # Build Ethernet frame from scratch
    │   ├── arp_request.py             # ARP protocol (who has this IP?)
    │   └── packet_sniffing.py         # Capture link-layer traffic

    │

    ├── 02-ip-layer/
    │   ├── ip_packet.c                # C: Build IP packet manually
    │   ├── ip_packet.py               # Scapy: Build IP packet
    │   ├── ping.py                    # ICMP echo request (ping)
    │   ├── traceroute.py              # Trace route with TTL manipulation
    │   └── fragmentation.py           # IP fragmentation demo
    │
    ├── 03-tcp-layer/
    │   ├── tcp_handshake.c            # C: Manual TCP SYN/SYN-ACK/ACK
    │   ├── tcp_handshake.py           # Scapy: Three-way handshake
    │   ├── tcp_server.py              # Python sockets: Simple TCP server
    │   ├── tcp_client.py              # Python sockets: Simple TCP client
    │   ├── tcp_retransmission.py     # Demonstrate packet loss & retransmit
    │   └── tcp_teardown.py            # FIN/ACK connection close

    │

    ├── 04-udp-layer/

    │   ├── udp_simple.py              # UDP packet construction

    │   ├── udp_vs_tcp.py              # Side-by-side comparison
    │   └── udp_broadcast.py           # Broadcast UDP packets
    │
    ├── 05-application-layer/
    │   ├── http/
    │   │   ├── http_request.py        # Build HTTP GET from scratch
    │   │   ├── http_server.py         # Minimal HTTP server
    │   │   └── http_over_tcp.py       # Show full HTTP/TCP/IP stack
    │   │
    │   ├── dns/
    │   │   ├── dns_query.py           # Build DNS query packet
    │   │   ├── dns_response.py        # Parse DNS response

    │   │   └── dns_server.py          # Minimal DNS server
    │   │

    │   └── ftp/
    │       ├── ftp_control.py         # FTP control channel
    │       └── ftp_data.py            # FTP data transfer
    │
    └── 06-security-layer/
        ├── tls_handshake.py           # Capture and analyze TLS handshake
        ├── certificate_chain.py       # Parse X.509 certificates
        └── https_request.py           # HTTPS vs HTTP comparison

```

## Documentation Format

**CRITICAL: Each source file includes comprehensive FAQ documentation**


Documentation is placed in each source file in this order:

1. **Imports/Includes** (`#include` or `import` statements)
2. **KEY CONCEPTS** - Brief bullet points of core concepts
3. **Code** - Functions and main execution
4. **FAQ** - Detailed Q&A section (always present, even if empty initially)

### Example Structure (Python)


```python
"""

TCP Three-Way Handshake


Demonstrates how TCP establishes a connection between client and server.
"""

from scapy.all import *

# ============================================================================
# KEY CONCEPTS
# ============================================================================
# - TCP connection requires 3-way handshake: SYN → SYN-ACK → ACK
# - SYN = synchronize (request connection)
# - ACK = acknowledgment (confirm receipt)
# - Sequence numbers track which bytes have been sent/received

# Configuration
TARGET = "example.com"
PORT = 80

# Build SYN packet
syn = IP(dst=TARGET)/TCP(dport=PORT, flags="S", seq=1000)

print("=== Sending SYN ===")
syn.show()

# Send and wait for SYN-ACK
syn_ack = sr1(syn, timeout=2)

if syn_ack and syn_ack.haslayer(TCP):
    print("\n=== Received SYN-ACK ===")
    syn_ack.show()
    
    # Send final ACK
    ack = IP(dst=TARGET)/TCP(
        dport=PORT, 
        flags="A",
        seq=syn_ack.ack,  # Our seq = their ack
        ack=syn_ack.seq + 1  # Our ack = their seq + 1
    )
    
    send(ack)
    print("\n=== Connection established ===")

# ============================================================================
# FREQUENTLY ASKED QUESTIONS
# ============================================================================
#

# 1. What exactly IS a "handshake"?
# ----------------------------------
# It's just three packets exchanged to establish a connection:
# 1. Client → Server: "I want to connect" (SYN)
# 2. Server → Client: "OK, I'm ready" (SYN-ACK)
# 3. Client → Server: "Got it, let's go" (ACK)
#
# After this, both sides agree the connection exists and data can flow.

#
#
# 2. Why can't we just start sending data immediately?
# ------------------------------------------------------
# TCP is reliable - it guarantees data arrives in order without corruption.
# To do this, both sides need to agree on:
# - Initial sequence numbers (where counting starts)
# - Window sizes (how much data can be sent at once)
# - Options (MSS, timestamps, etc.)
#
# The handshake establishes these parameters before data flows.

#
#
# 3. What are sequence numbers for?
# ----------------------------------
# They track which bytes have been sent/received. Example:
# - Client sends bytes 1000-1100 (seq=1000)
# - Server replies: "Got it, send 1101 next" (ack=1101)

# - Client sends bytes 1101-1200 (seq=1101)
#
# If packets arrive out of order, sequence numbers let TCP reassemble them.
#
#
# 4. Why does the ACK value = seq + 1?
# -------------------------------------
# The SYN packet itself consumes one sequence number (even though it carries
# no data). So if Server sends SYN with seq=5000, the next expected byte is
# 5001, which is what Client acknowledges.

#
# This is a TCP quirk - SYN and FIN flags consume sequence numbers.
```

### Example Structure (C)

```c
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>


/*
 * ============================================================================
 * KEY CONCEPTS
 * ============================================================================
 * - Raw sockets require manual header construction
 * - struct iphdr = IP header (20 bytes minimum)
 * - struct tcphdr = TCP header (20 bytes minimum)
 * - Checksums prevent packet corruption
 * - Network byte order = big-endian (use htons/htonl)
 */

// Code starts here

void build_tcp_packet() {
    // Manual header construction
}

int main() {

    build_tcp_packet();
    return 0;
}

/*
 * ============================================================================
 * FREQUENTLY ASKED QUESTIONS

 * ============================================================================
 *
 * 1. Why do we need htons() and htonl()?
 * ---------------------------------------
 * Network protocols use big-endian byte order, but most CPUs (x86) use
 * little-endian. These functions convert:
 * - htons() = "host to network short" (16-bit values like ports)
 * - htonl() = "host to network long" (32-bit values like IP addresses)
 *
 * Without conversion, a port number 80 (0x0050) might be sent as 0x5000,
 * which the receiver interprets as port 20480.
 *

 *
 * 2. What is a raw socket and why do we need root privileges?
 * ------------------------------------------------------------
 * Normal sockets (SOCK_STREAM, SOCK_DGRAM) let the OS build headers for you.

 * Raw sockets (SOCK_RAW) give you direct access to build packets from scratch.
 *
 * Root is required because:
 * - You can forge source IP addresses (spoofing)

 * - You can craft malicious packets
 * - Security risk if any user could do this
 */
```

## FAQ Guidelines

### Be Proactive About Documentation


After answering user questions, **actively check if the conversation should be documented**:


1. **Review existing FAQ section** - Check if this topic is already covered
2. **Assess if it's documentable** - Did the user express confusion or ask "why"?
3. **Offer to document it** - Don't wait. Say: "Should I add this to the FAQ?"
4. **Think like a beginner** - Would someone new find this confusing? Document it.

### What to Document

**DO document (✅):**
- Concepts the user actually asked about or was confused by
- Syntax questions ("What does `flags='S'` mean?")

- "Why" questions (why three-way handshake? why checksums?)
- Common gotchas (byte order, permissions, etc.)
- Things that seem "obvious" to experts but confusing to newcomers

**DON'T document (❌):**
- Concepts the user didn't ask about (don't add noise)
- Things that are obvious to the user already

- Generic Python/C knowledge unrelated to networking

### Inline Comments vs FAQ

**Inline comments** - Use for line-specific explanations:

```python
# ACK number = their sequence + 1 (TCP quirk: SYN consumes a sequence number)
ack=syn_ack.seq + 1
```


**FAQ section** - Use for broader conceptual questions:
```python
# 5. Why does TCP have a separate "close" handshake?
# ---------------------------------------------------
# [Full explanation here]

```

### When User Asks Questions

1. **Answer directly first** - Give the actual answer, no fluff
2. **Determine location** - Is this line-specific or conceptual?
3. **Extract the essence** - Rewrite question concisely
4. **Add documentation** - Inline comment OR FAQ entry

5. **Number sequentially** - Each FAQ gets a number
6. **Ask if user wants it documented** - "Should I add this to the FAQ?"

### Example Transformation

User asks:
> "Wait so why do we need to do `sr1()` instead of just `send()`? What's the difference?"


Add to FAQ as:
```python
# 3. What's the difference between send() and sr1()?

# ---------------------------------------------------
# - send() = fire and forget (just sends packet, doesn't wait for response)
# - sr1() = send and receive 1 packet (waits for a response, returns it)
#
# Use send() when you don't care about replies (e.g., final ACK in handshake)
# Use sr1() when you need the response (e.g., waiting for SYN-ACK)
```

## Tabula Rasa Questioning

**The user can ask ANY question, no matter how basic, at ANY time.**

Examples of "stupid" questions that are ENCOURAGED:
- "What exactly is a byte?"
- "Why are there 8 bits in a byte?"
- "What does 'big-endian' mean?"
- "What's the difference between a pointer and a variable?"
- "Why do we use hexadecimal instead of decimal?"
- "What does 'network stack' mean?"
- "What's a checksum and why do we need it?"

**Response style:**
- ✅ Direct, clear explanations without condescension
- ✅ Use analogies when helpful
- ✅ Show code examples
- ✅ Explain "why" not just "what"

- ✅ Always offer to add to FAQ after answering
- ❌ Never say "great question!" or similar fluff
- ❌ Never make the user feel bad for not knowing

- ❌ No excessive enthusiasm or marketing-speak

## Core Requirements


### 1. Every Example Must Include

**Code file:**

- Minimal, focused implementation
- Heavily commented explaining each field
- KEY CONCEPTS section at top
- FAQ section at bottom (even if empty initially)
- Runnable with single command


**Output visualization:**
- Raw hex dump of packet
- Decoded headers (field by field)
- Expected behavior vs actual result

**Documentation:**
- What this demonstrates (1 sentence)
- Prerequisites (permissions, setup)
- Run instructions (copy-paste ready)
- Sample output (actual terminal output)
- What to observe ("notice bytes 4-7 are the sequence number")

### 2. Packet Visualization Format

Every example should output something like:

```
=== Building TCP SYN Packet ===

Packet Structure:
IP Layer:
  Version: 4
  Header Length: 20 bytes
  Source IP: 192.168.1.100
  Dest IP: 93.184.216.34
  
TCP Layer:

  Source Port: 54321
  Dest Port: 80
  Sequence Number: 1000
  Flags: SYN

  Window Size: 65535

Hex Dump:
0000   45 00 00 3C 1C 46 40 00 40 06 B1 E6 C0 A8 01 64
0010   5D B8 D8 22 D4 31 00 50 00 00 03 E8 00 00 00 00
0020   A0 02 FF FF 76 DF 00 00 02 04 05 B4 04 02 08 0A

Decoded:
Bytes 0-3: IP header (version=4, length=20, etc.)
Bytes 14-15: TCP source port (54321)
Bytes 16-17: TCP dest port (80)
Bytes 18-21: Sequence number (1000)

Sending packet...
Response received:
[Show response with same level of detail]
```

### 3. Progression Path

**Week 1: Foundations**
- `00-foundations/`: Understand raw sockets in C, then move to Python
- Show that protocols are just byte formats with rules


**Week 2: Lower Layers**  
- `01-link-layer/`: Ethernet, ARP
- `02-ip-layer/`: IP packets, ICMP (ping), routing

**Week 3: Transport Layer**
- `03-tcp-layer/`: Handshake, reliability, connection management
- `04-udp-layer/`: Connectionless, fast, unreliable

**Week 4: Application Layer**
- `05-application-layer/`: HTTP, DNS, FTP built on top of TCP/UDP

**Week 5: Security**
- `06-security-layer/`: TLS/SSL, HTTPS, encryption

## Specific Examples to Implement


### Foundation: The Hard Way (C)

**`00-foundations/raw_socket.c`**
```c
// Create raw socket
// Manually pack IP header (20 bytes)
// Manually pack TCP header (20 bytes)  
// Calculate checksums
// Send packet
// Show every field as you build it
```

**`00-foundations/same_in_scapy.py`**
```python

# Same exact packet in 3 lines of Scapy
# Show how abstractions help
```

### TCP Three-Way Handshake

**`03-tcp-layer/tcp_handshake.py`**
- Send SYN packet, show exact bytes
- Receive SYN-ACK, decode it field-by-field
- Send ACK, complete handshake

- Log sequence/acknowledgment number evolution

### HTTP Request Breakdown

**`05-application-layer/http/http_over_tcp.py`**
- Build HTTP GET request as string
- Show TCP segmentation of HTTP data
- Show IP encapsulation of TCP segments
- Visualize each layer wrapping the previous

### DNS Query from Scratch

**`05-application-layer/dns/dns_query.py`**
- Build DNS query packet manually
- Show binary format (header, question, answer sections)
- Send to 8.8.8.8
- Parse response byte-by-byte


### TLS Handshake Analysis


**`06-security-layer/tls_handshake.py`**

- Capture TLS handshake with Scapy
- Show ClientHello, ServerHello messages
- Display certificate exchange
- Show where encryption starts

## Documentation Standards

### `tcp-ip-vs-osi.md`
```markdown
# TCP/IP vs OSI: Why We Use TCP/IP

## The Short Answer

**TCP/IP** = what the internet actually uses (reality)  
**OSI** = academic theory from the 1980s (never fully implemented)

## TCP/IP Model (4 layers) - REALITY

```
Application  →  HTTP, DNS, FTP, SSH, etc.
Transport    →  TCP, UDP
Internet     →  IP, ICMP
Link         →  Ethernet, WiFi
```


## OSI Model (7 layers) - THEORY

```
Application   →  HTTP, FTP
Presentation  →  ??? (data formats, encryption maybe?)
Session       →  ??? (connection management, but TCP does this?)
Transport     →  TCP, UDP
Network       →  IP
Data Link     →  Ethernet
Physical      →  Cables, radio
```

## Why OSI Is Taught (But Not Used)

Schools teach OSI because it's more "complete" theoretically. But:
- Layers 5-6 (Session/Presentation) are vague
- Nobody agrees what belongs in these layers
- The internet already existed using TCP/IP when OSI was created
- No major implementation of OSI ever succeeded


## What This Repo Uses

We use **TCP/IP** because that's reality. Every example, every protocol,
every packet in this repo follows the TCP/IP model.
```

### `what-is-a-protocol.md`

```markdown
# What Is a Protocol?

A protocol is just an agreement about what bytes mean.


## Example: Imaginary Message Protocol

```
Byte 0:      Message type (1=hello, 2=goodbye)
Bytes 1-2:   Message length
Bytes 3-10:  Sender name (8 characters)
Bytes 11+:   Message content
```

If I send you these bytes:
```
01 00 0C 41 6C 69 63 65 00 00 00 48 69 21
```


You decode it as:
- Byte 0 = `01` → Type 1 (hello)

- Bytes 1-2 = `00 0C` → Length 12
- Bytes 3-10 = `41 6C 69 63 65 00 00 00` → "Alice"
- Bytes 11+ = `48 69 21` → "Hi!"

That's it. A protocol is just rules about byte positions and meanings.


## Real Protocols Work the Same Way


TCP header:
```
Bytes 0-1:   Source port
Bytes 2-3:   Destination port
Bytes 4-7:   Sequence number
Bytes 8-11:  Acknowledgment number
...
```

No magic. Just specifications.

```

## Utilities to Provide

**`utils/packet_visualizer.py`**
```python
def visualize_packet(packet):
    """
    Takes a Scapy packet, outputs:
    - Layer-by-layer summary
    - Hex dump with annotations
    - Decoded fields
    """
    # Implementation

```

**`utils/capture.py`**
```python
def capture_traffic(filter="tcp port 80", count=10):
    """
    Wrapper around Scapy sniff()
    - Saves to pcap file
    - Prints live summary
    - Returns packets for analysis
    """
    # Implementation

```

## Key Concepts to Demonstrate

1. **Protocols are just structured bytes**
2. **Headers add metadata at each layer**
3. **Encapsulation: each layer wraps the previous**
4. **Checksums prevent corruption**
5. **Sequence numbers enable ordering and reliability**
6. **Ports multiplex multiple connections**
7. **Flags control connection state (SYN, ACK, FIN)**

## Constraints


- Each example runs in <30 seconds
- Minimal external dependencies (Scapy, standard lib)
- No theory without runnable code

- Every concept has visible output (hex dumps, decoded packets)
- Progressive complexity (don't jump to TLS before understanding TCP)
- **FAQ section in every source file, even if empty initially**
- **Expect and encourage "basic" questions from user**

## Success Criteria

By the end of this repo, a learner should be able to:
- Explain what happens at each layer when they visit a website
- Build a TCP connection from scratch using Scapy
- Debug network issues by reading packet captures
- Understand what "protocol" actually means (byte specifications)
- Read RFCs and implement simple protocols
- Ask ANY question without feeling stupid
- Have a comprehensive FAQ for each concept they struggled with

Start with `00-foundations/raw_socket.c` to show the hard way, then immediately show the same thing in Scapy. Build up from there. Document every question the user asks in the appropriate source file.
