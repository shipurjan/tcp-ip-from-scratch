# TCP/IP From Scratch

**A visual explanation of the TCP/IP model for web developers.**

Learn what actually happens when you make an HTTP request by seeing the actual bytes at each protocol layer.

## What Is This?

Most networking tutorials explain concepts abstractly. This repo shows you **exactly what protocols are**: byte formats with rules.

When you visit a website, your browser doesn't send "HTTP magic" - it sends specific bytes in a specific order. This repo shows you:
- What those bytes look like (hex dumps)
- What each byte means (field-by-field breakdowns)
- How HTTP becomes TCP becomes IP becomes Ethernet
- Why HTTPS uses different ports and what encryption looks like

**Designed for web developers** who want to understand the layers beneath their HTTP requests and API calls.

## Approach

**Visual, byte-level explanations designed for web developers.**

Every example:
1. Shows hex dumps of actual packets
2. Breaks down exactly what each byte means
3. Visualizes how layers wrap each other
4. Includes FAQ sections answering real questions from development

Focus areas:
- **Application Layer** (HTTP, JSON, DNS, FTP) - what you work with daily
- **Transport Layer** (TCP, UDP) - understanding ports, connections, reliability
- **TLS/HTTPS** - why encryption matters and how it works
- **IP and Ethernet** - just enough to understand the full picture

**No emojis, no fluff, no theory without hex dumps.** Just clear explanations of what the bytes actually are.

## Tech Stack

- **Python + Scapy** - Clean packet manipulation and visualization
- **Wireshark/tcpdump** (optional) - For packet capture analysis

Every example is a single Python file using Scapy. No C, no compilation, no complexity.

## Learning Path

This repo follows the **TCP/IP model** (4 layers) because that's what the internet actually uses:

```
┌─────────────────────────────────────────┐
│  Application Layer                      │  HTTP, DNS, FTP
│  (What applications use)                │
├─────────────────────────────────────────┤
│  Transport Layer                        │  TCP, UDP
│  (Port-to-port communication)           │
├─────────────────────────────────────────┤
│  Internet Layer                         │  IP, ICMP
│  (Host-to-host routing)                 │
├─────────────────────────────────────────┤
│  Link Layer                             │  Ethernet, ARP
│  (Physical network access)              │
└─────────────────────────────────────────┘
```

### Examples

1. **Foundations** (`01-foundations.py`) - All 4 TCP/IP layers explained
   - Application Layer: HTTP, JSON, DNS, FTP, email, files
   - Transport Layer: TCP and UDP with real-world examples
   - Internet Layer: IP routing and addressing
   - Link Layer: Ethernet frames and MAC addresses
   - Complete 4-layer packet demonstration
   - Comprehensive FAQ covering layer interactions

2. **TLS and HTTPS** (`02-tls-https.py`) - Encryption in action
   - HTTP vs HTTPS comparison (readable vs encrypted hex dumps)
   - TLS handshake process (ClientHello, ServerHello)
   - Port differences (80 vs 443) and why they matter
   - Cipher suites and encryption algorithms
   - Session persistence and key reuse
   - FAQ covering TLS/SSL fundamentals

## Example Output

What you'll see when running examples:

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
Bytes 0-3: IP header (version=4, length=20)
Bytes 14-15: TCP source port (54321 = 0xD431)
Bytes 16-17: TCP dest port (80 = 0x0050)
Bytes 18-21: Sequence number (1000 = 0x000003E8)
Bytes 22-25: Acknowledgment number (0)
```

Every byte has a purpose. Every field has a meaning. You'll see them all.

## Setup

### Prerequisites

- Python 3.12+
- Any operating system (Linux, macOS, Windows)
- No root/sudo access needed (examples build packets in memory)

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/tcp-ip-from-scratch.git
cd tcp-ip-from-scratch

# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Test Scapy works
uv run python -c "from scapy.all import *; print('Scapy ready!')"
```

## Running Examples

### Basic Usage

All examples are single Python files in the `examples/` directory.

```bash
# Run the foundations example (covers all 4 layers)
uv run python examples/01-foundations.py

# Run the TLS/HTTPS example (encryption and security)
uv run python examples/02-tls-https.py
```

Note: These examples build packets in memory and don't require sudo/root access.

### Optional: Monitoring Real Traffic

To see real HTTPS traffic on your system (optional learning exercise):

```bash
# Capture HTTPS handshakes (requires sudo)
sudo tcpdump -i any -X port 443

# You'll see ClientHello, ServerHello, and encrypted data
# Compare with the hex dumps from 02-tls-https.py
```

### Example Workflow

1. **Start with foundations:** Run `examples/01-foundations.py`
2. **Read the code:** Open the file and read the KEY CONCEPTS section
3. **Observe output:** See packet structures, hex dumps, and decoded fields for all 4 layers
4. **Read FAQ:** Check the FAQ section at the end for answers to common questions
5. **Move to TLS:** Run `examples/02-tls-https.py` to understand encryption
6. **Experiment:** Modify values (IP addresses, ports, cipher suites) and re-run

## Repository Structure

```
tcp-ip-from-scratch/
├── examples/
│   ├── 01-foundations.py      # All 4 TCP/IP layers with examples
│   └── 02-tls-https.py        # TLS/HTTPS encryption and security
│
├── CLAUDE.md                  # Development guidelines
├── README.md                  # This file
└── pyproject.toml             # uv dependencies (scapy, dev tools)
```

## How to Use This Repo

1. **Start with foundations** - Run `examples/01-foundations.py` to see all 4 layers
2. **Read the output** - See hex dumps, byte breakdowns, and layer visualizations
3. **Understand the FAQs** - Read the FAQ section at the end of each file
4. **Move to encryption** - Run `examples/02-tls-https.py` to see TLS in action
5. **Experiment** - Modify examples. Change ports, IPs, data. See what happens.
6. **Ask questions** - No question is too basic. The FAQs came from real questions.

## Philosophy

### Questions Are Encouraged

Ask **any** question, no matter how basic:
- "What exactly is a byte?"
- "Why are there 8 bits in a byte?"
- "What does 'big-endian' mean?"
- "What's a checksum and why do we need it?"

If you're confused about something, **it should be documented**. Many FAQs in source files came from real questions.

### No Theory Without Code

Protocols aren't abstract concepts - they're byte formats. Every explanation includes:
- Runnable code that constructs the protocol
- Hex dumps showing the actual bytes
- Decoded output explaining each field
- Expected behavior vs actual result

### Reality Over Theory

This repo uses the **TCP/IP model** (4 layers), not the OSI model (7 layers), because that's what the internet actually uses.

## What You'll Learn

By working through these examples, you'll understand:
- What happens at each of the 4 TCP/IP layers when you visit a website
- How protocols are just structured bytes with agreed-upon field layouts
- The difference between TCP (reliable) and UDP (fast)
- How HTTP requests become TCP segments, IP packets, and Ethernet frames
- Why HTTPS uses port 443 instead of 80
- The difference between TCP handshake (connection) and TLS handshake (encryption)
- How encryption makes data unreadable to attackers
- Why one handshake can handle many HTTP requests (persistent connections)
- What ClientHello, ServerHello, and cipher suites actually are

## Built With Claude Code

This repository was built interactively using [Claude Code](https://claude.com/claude-code), an AI-powered CLI tool. Each example was developed iteratively:
- Ask questions about networking concepts
- Implement examples with immediate feedback
- Debug packet construction in real-time
- Document confusion points as FAQs

The FAQ sections in each file came from real questions asked during development.

## Contributing

Found a bug? Have a question that should be in a FAQ? Want to add an example?

Open an issue or pull request. The best contributions:
- Add examples that show bytes/packets
- Answer questions in FAQ sections
- Identify confusing concepts that need better explanation
- Fix errors in packet construction or field descriptions

## Resources

- [Scapy Documentation](https://scapy.readthedocs.io/)
- [TCP/IP RFCs](https://www.rfc-editor.org/) - Official protocol specifications
- [Wireshark User Guide](https://www.wireshark.org/docs/wsug_html_chunked/)

## License

MIT License - See LICENSE file for details

---

**Remember**: Protocols are just bytes. This repo shows you which bytes go where and why.
