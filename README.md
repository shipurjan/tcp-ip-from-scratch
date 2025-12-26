# TCP/IP From Scratch

Learn networking protocols by implementing them from scratch and seeing the actual bytes.

## What Is This?

Most networking tutorials explain concepts abstractly. This repo shows you **exactly what protocols are**: byte formats with rules.

When you visit a website, your browser doesn't send "HTTP magic" - it sends specific bytes in a specific order. This repo shows you:
- What those bytes look like
- What each byte means
- How to construct them yourself
- How to decode them when you receive them

## Approach

**See the bytes, understand the protocol.**

Every example in this repo:
1. Builds packets from scratch (using Python + Scapy)
2. Shows hex dumps with decoded fields
3. Visualizes each protocol layer
4. Includes comprehensive FAQ sections for common questions

**No theory without runnable code.** If you can't see it in action, it's not here.

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

### Progression

1. **Foundations** (`00-foundations.py`) - Build raw TCP packets with Scapy
2. **Link Layer** (`01-ethernet.py`, `02-arp.py`) - Ethernet frames, ARP
3. **Internet Layer** (`03-ip-packet.py`, `04-icmp-ping.py`, `05-traceroute.py`) - IP, ICMP, routing
4. **Transport Layer** (`06-tcp-handshake.py`, `10-udp-simple.py`) - TCP and UDP
5. **Application Layer** (`12-http-request.py`, `13-dns-query.py`) - HTTP, DNS
6. **Security Layer** (`15-tls-handshake.py`) - TLS/SSL analysis

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

- Python 3.8+
- Linux or macOS (recommended for raw socket access)
- Root/sudo access (required for raw sockets and packet capture)

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
sudo $(which uv) run python -c "from scapy.all import *; print('Scapy ready!')"
```

For detailed setup instructions, see `setup/install.md` and `setup/permissions.md`.

## Running Examples

### Basic Usage

All examples are single Python files in the `examples/` directory.

```bash
# Run any example with sudo (required for raw sockets)
sudo $(which uv) run python examples/00-foundations.py
sudo $(which uv) run python examples/06-tcp-handshake.py
sudo $(which uv) run python examples/13-dns-query.py
```

### Monitoring Traffic

Open a second terminal to watch packets being sent:

```bash
# Watch all traffic on loopback interface
sudo tcpdump -i lo -X

# Watch specific port (e.g., HTTP on port 80)
sudo tcpdump -i lo -X port 80

# Watch DNS queries
sudo tcpdump -i lo -X port 53
```

### Example Workflow

1. **Choose an example:** Start with `00-foundations.py`
2. **Read the code:** Open the file and read the KEY CONCEPTS section
3. **Run it:** Execute with `sudo $(which uv) run python examples/00-foundations.py`
4. **Observe output:** See the packet structure, hex dump, and decoded fields
5. **Experiment:** Modify values (IP addresses, ports, flags) and re-run
6. **Read FAQ:** Check the FAQ section in the source file for common questions

## Repository Structure

```
tcp-ip-from-scratch/
├── examples/                  # All runnable examples (single .py files)
│   ├── 00-foundations.py      # Raw packet construction
│   ├── 01-ethernet.py         # Ethernet frames
│   ├── 02-arp.py              # Address Resolution Protocol
│   ├── 03-ip-packet.py        # IP packet construction
│   ├── 04-icmp-ping.py        # ICMP echo (ping)
│   ├── 06-tcp-handshake.py    # TCP three-way handshake
│   ├── 10-udp-simple.py       # UDP basics
│   ├── 12-http-request.py     # HTTP over TCP/IP
│   ├── 13-dns-query.py        # DNS queries
│   └── 15-tls-handshake.py    # TLS/SSL analysis
│
├── utils/                     # Packet visualization and capture helpers
├── docs/                      # Conceptual guides
└── pyproject.toml             # uv dependencies
```

## How to Use This Repo

1. **Start with foundations** - Run `examples/00-foundations.py` to see raw packet construction
2. **Follow the progression** - Go through directories in order (00 → 01 → 02 → ...)
3. **Run every example** - Don't just read the code. Execute it. See the output.
4. **Read the FAQs** - Every source file has a FAQ section answering common questions
5. **Experiment** - Modify examples. Break things. See what happens.
6. **Ask questions** - No question is too basic. Document confusion in FAQs.

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

This repo uses the **TCP/IP model** (4 layers), not the OSI model (7 layers), because that's what the internet actually uses. See `docs/tcp-ip-vs-osi.md` for details.

## What You'll Learn

By working through this repo, you'll be able to:
- ✅ Explain what happens at each layer when you visit a website
- ✅ Build TCP connections from scratch using Scapy
- ✅ Read packet captures and identify issues
- ✅ Understand what "protocol" actually means (agreed-upon byte formats)
- ✅ Debug network problems by examining raw packets
- ✅ Read RFCs and implement simple protocols
- ✅ See the difference between what frameworks do and what actually goes on the wire

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
- `docs/reading-rfcs.md` - How to read protocol specifications
- `docs/wireshark-guide.md` - Capturing and analyzing traffic

## License

MIT License - See LICENSE file for details

---

**Remember**: Protocols are just bytes. This repo shows you which bytes go where and why.
