# Network Protocol Learning Repository - Implementation Prompt

I want to build a GitHub repository that teaches networking protocols by implementing them from scratch using Python and Scapy. The goal is to show EXACTLY what each protocol is - the actual bytes, headers, and data structures - not just conceptual explanations.

## Tech Stack

**Python + Scapy (100% of examples)**

- Packet manipulation, visualization, and capture
- Clear field-by-field packet construction
- Interactive experimentation
- Shows the actual bytes while handling tedious details
- Runnable examples with immediate feedback

## Repository Structure

```
tcp-ip-from-scratch/
│
├── README.md                          # Overview, setup, learning path
├── pyproject.toml                     # Poetry dependencies (Scapy)
│
├── utils/
│   ├── packet_visualizer.py           # Hex dump + decoded headers
│   ├── capture.py                     # Packet capture wrapper
│   └── helpers.py                     # Common utilities
│
├── docs/
│   ├── what-is-a-protocol.md          # Protocols = agreed byte formats
│   ├── tcp-ip-vs-osi.md               # Why we use TCP/IP model
│   ├── reading-rfcs.md                # How to read protocol specs
│   └── wireshark-guide.md             # Capturing and analyzing traffic
│
└── examples/
    ├── 00-foundations.py              # Raw TCP SYN packet
    ├── 01-ethernet.py                 # Ethernet frames
    ├── 02-arp.py                      # ARP protocol
    ├── 03-ip-packet.py                # IP packet construction
    ├── 04-icmp-ping.py                # ICMP echo (ping)
    ├── 05-traceroute.py               # TTL manipulation
    ├── 06-tcp-handshake.py            # TCP three-way handshake
    ├── 07-tcp-data.py                 # TCP data transfer
    ├── 08-tcp-retransmission.py       # Packet loss handling
    ├── 09-tcp-teardown.py             # Connection close
    ├── 10-udp-simple.py               # UDP basics
    ├── 11-udp-broadcast.py            # UDP broadcasting
    ├── 12-http-request.py             # HTTP over TCP/IP
    ├── 13-dns-query.py                # DNS resolution
    ├── 14-dns-server.py               # Minimal DNS responder
    └── 15-tls-handshake.py            # TLS/SSL analysis
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


## FAQ Guidelines

### CRITICAL: Start with Empty FAQs

**FAQs must start EMPTY and only be populated when the user actually asks questions.**

- ❌ DO NOT preemptively add FAQs that seem "useful" or "common"
- ❌ DO NOT add FAQs just because they might help future readers
- ✅ ONLY add FAQs when the user explicitly asks a question
- ✅ Keep FAQ sections empty (with placeholder) until user asks

**IMPORTANT: FAQs are printed for website publishing**

Program output will be published on a website, so FAQs must be in the **PRINTED OUTPUT ONLY**.

- ✅ Add FAQs as print statements (for website visitors)
- ❌ Do NOT add FAQ in code comments (outdated approach)
- ✅ Important educational content goes in print statements
- ✅ Code comments are for explaining the code itself (how it works)

Example structure:
```python
# At end of program:
print("\n\n\n\n")  # 5 newlines for spacing

section_sep()
print("FREQUENTLY ASKED QUESTIONS")
section_sep()
print("\n(No questions yet - ask away!)\n")
section_sep()
```

When user asks a question, add it to the printed FAQ:
```python
print("\n📖 Q: What does TTL mean?")
example_sep()
print("""
TTL = Time to Live. It's the maximum number of hops (routers) a packet
can traverse before being discarded.

Each router decrements TTL by 1. When TTL reaches 0, the packet is dropped.
This prevents packets from circulating forever in routing loops.
""")
```

### Program Output vs Code Comments

**CRITICAL: Program output should NEVER mention Scapy or the tool being used.**

The program output teaches protocols (TCP/IP), not Scapy. Keep output focused on:
- What the protocol is
- What fields it contains
- What the bytes look like
- How protocols work

**DO (✅):**
```python
print("TCP provides reliable, ordered delivery")
print("Checksums are calculated automatically")
# Comment: Scapy calculates these for us
```

**DON'T (❌):**
```python
print("Scapy handles checksums for you")
print("The '/' operator in Scapy means encapsulate")
```

Scapy mentions belong ONLY in:
- Code comments (to explain the code)
- Variable names (if needed)
- Not in print() statements

### Be Proactive About Documentation (When User Asks)

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

### Code Comments vs Printed FAQ

**Code comments** - Use for explaining HOW the code works:

```python
# Build packet and convert to bytes to trigger field calculations
packet = IP(bytes(packet))
```

**Printed FAQ** - Use for broader conceptual questions users ask:
```python
print("\n📖 Q: Why does TCP have a separate 'close' handshake?")
example_sep()
print("""
[Full explanation here - will appear on website]
""")
```

### When User Asks Questions

1. **Answer directly first** - Give the actual answer, no fluff
2. **Determine if it should be documented** - Is this genuinely confusing?
3. **Extract the essence** - Rewrite question concisely
4. **Add to printed FAQ** - So it appears on website
5. **Ask if user wants it documented** - "Should I add this to the FAQ?"

Important:
- Code comments explain the code (for developers reading source)
- Printed FAQ explains protocols (for website visitors learning TCP/IP)

### Example Transformation

User asks:
> "Wait so why do we need to do `sr1()` instead of just `send()`? What's the difference?"

Add to printed FAQ as:
```python
print("\n📖 Q: What's the difference between send() and sr1()?")
example_sep()
print("""
send() = Fire and forget
  • Just sends the packet
  • Doesn't wait for response
  • Use when you don't need a reply

sr1() = Send and receive 1 packet
  • Sends packet and waits for response
  • Returns the first matching reply
  • Use when you need the response (like ping, or TCP handshake)
""")
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
- `00-foundations.py`: Build raw TCP packets with Scapy
- Show that protocols are just byte formats with rules
- Understand what Scapy does behind the scenes


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


### Foundation: Understanding Raw Packets

**`00-foundations.py`**
```python
# Build a TCP SYN packet using Scapy
# Show every field in the packet
# Display hex dump and decoded headers
# Understand encapsulation (TCP inside IP)
# Demonstrate what Scapy handles automatically:
# - Checksums (IP and TCP)
# - Network byte order
# - Header length calculations
# - Protocol field values
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

Start with `00-foundations.py` to demonstrate raw packet construction with Scapy. Build up from there, progressing through each layer of the TCP/IP model. Document every question the user asks in the appropriate source file's FAQ section.
