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
├── examples/
│   ├── 01-foundations.py              # All 4 TCP/IP layers with examples
│   └── 02-tls-https.py                # TLS/HTTPS encryption and security
│
├── CLAUDE.md                          # Development guidelines (this file)
├── README.md                          # User-facing documentation
└── pyproject.toml                     # uv dependencies (scapy, dev tools)
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

## Implemented Examples

### Example 01: Foundations (`01-foundations.py`)

Comprehensive introduction to all 4 TCP/IP layers:

**Layer 4 - Application Layer:**
- 9 examples: HTTP, JSON, DNS, FTP, email, plain text, binary data, CSV
- Shows that all application data is "just bytes" to lower layers

**Layer 3 - Transport Layer:**
- TCP: 5 examples showing different flags (SYN, SYN-ACK, ACK, PSH-ACK, FIN-ACK)
- UDP: 4 examples (DNS, streaming, DHCP, NTP)
- Byte-by-byte hex breakdowns showing where port numbers, sequence numbers are encoded
- TCP vs UDP comparison

**Layer 2 - Internet Layer:**
- IP packet structure with routing fields
- Shows how IP doesn't care about TCP vs UDP

**Layer 1 - Link Layer:**
- Ethernet frame with MAC addresses
- Explains local vs remote delivery

**4-Layer Composed Packet:**
- Complete HTTP request with all layers: `Ether() / IP() / TCP() / Raw(HTTP)`
- Full hex dump showing ~95 bytes
- Key byte highlights for each layer
- Encapsulation visualization

**FAQ Section:**
- What is HTTP? (it's the text syntax itself)
- Do all packets need all 4 layers? (no - depends on use case)
- Who adds headers? (application + OS, not routers)
- Headers vs trailers? (Ethernet has both, others just headers)
- Which devices need which layers? (app=Layer 4, OS=Layers 2-3, routers=Layers 1-2)
- Why TCP handshake? (once per connection, not per request)

### Example 02: TLS and HTTPS (`02-tls-https.py`)

Encryption and security explanation:

**Introduction:**
- Where TLS fits (between TCP and HTTP)
- Why different ports (80 vs 443)
- What ClientHello and ServerHello are (TLS messages, not TCP flags)

**Demo 1 - Plain HTTP:**
- Complete packet: `TCP(dport=80) / Raw(HTTP with password)`
- Hex dump shows readable password
- Demonstrates security risk

**Demo 2 - Encrypted HTTPS:**
- Complete packet: `TCP(dport=443) / Raw(TLS encrypted data)`
- 8-step encryption process explained
- Hex dump shows gibberish (unreadable)
- TLS record structure breakdown

**Demo 3 - TLS Handshake:**
- Two handshakes explained (TCP first, then TLS)
- TLS handshake steps: ClientHello, ServerHello, Certificate, Key Exchange, Finished
- ClientHello packet construction with cipher suites
- Difference between TCP flags vs TLS messages

**Cipher Suites:**
- Breakdown of cipher suite components
- Example: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256

**FAQ Section:**
- What does S in HTTPS stand for? (Secure)
- What is TLS vs SSL? (SSL deprecated, TLS is current)
- What other protocols use TLS? (FTPS, SMTPS, IMAPS, POP3S)
- Does every request need new TLS handshake? (no - once per TCP connection)

## Key Concepts Demonstrated

1. **Protocols are just structured bytes** - hex dumps prove it
2. **Encapsulation: each layer wraps the previous** - visualized with ASCII diagrams
3. **TCP provides reliability** - checksums, sequence numbers, ACKs, retransmission
4. **Ports identify applications** - 80=HTTP, 443=HTTPS, 53=DNS, etc.
5. **Encryption makes data unreadable** - visual comparison of hex dumps
6. **Handshakes happen once per connection** - persistent connections reuse TCP and TLS sessions
7. **Lower layers don't understand higher layers** - IP doesn't care about TCP vs UDP

## Design Principles

- **Visual focus**: Every concept shown with hex dumps
- **Web developer audience**: Focus on Application and Transport layers
- **No emojis**: Clean, professional output
- **FAQ from real questions**: Only add when user asks
- **Printed FAQs**: For website publishing, not code comments
- **No Scapy mentions in output**: Teach protocols, not tools
- **71-character separators**: Match hexdump width

## Current Scope

The repository is **complete** with 2 comprehensive examples covering:
- All 4 TCP/IP layers
- TCP and UDP transport protocols
- TLS/HTTPS encryption and security
- Real-world use cases (web, email, DNS, streaming)
- Comprehensive FAQs answering actual questions from development

Additional examples (Ethernet, ARP, ICMP, etc.) can be added in the future if needed, but the current examples provide a solid foundation for web developers to understand networking fundamentals.
