"""
TCP SYN Packet Using Scapy

Foundation: Understanding raw packet construction.
Demonstrates building a TCP SYN packet from scratch,
showing every field and byte in the packet.
"""

from scapy.all import IP, TCP, send, hexdump, conf
import sys

# ============================================================================
# KEY CONCEPTS
# ============================================================================
# - Protocols are just structured bytes with agreed-upon meanings
# - Scapy handles all header construction automatically
# - Checksums calculated for you (IP and TCP)
# - Field values have sensible defaults (version=4, ttl=64, etc.)
# - Can override any field if needed
# - Raw sockets require root privileges (security)
# - '/' operator layers protocols (IP / TCP means "TCP inside IP")
# - Every field can be inspected and modified

# Disable verbose output for cleaner demo
conf.verb = 0

print("=== Building TCP SYN Packet (Scapy) ===\n")

# ============================================================================
# BUILD PACKET
# ============================================================================

# This creates a complete 40-byte TCP SYN packet
# IP layer + TCP layer = complete packet
packet = IP(src="127.0.0.1", dst="127.0.0.1") / TCP(
    sport=54321,
    dport=80,
    flags="S",
    seq=1000
)

# Scapy automatically fills in:
# - IP version (4)
# - IP header length (20 bytes)
# - IP total length (40 bytes)
# - IP TTL (64)
# - IP protocol (6 for TCP)
# - IP checksum
# - TCP data offset (5 for 20 bytes)
# - TCP window size (8192 by default, but we can override)
# - TCP checksum
# - TCP acknowledgment (0 for SYN)

# Override window size (default is 8192)
packet[TCP].window = 65535

# ============================================================================
# DISPLAY PACKET STRUCTURE
# ============================================================================

print("--- Packet Structure (Scapy's .show() method) ---")
packet.show()

# Build the packet to calculate automatic fields (checksums, lengths, etc.)
packet = IP(bytes(packet))

# ============================================================================
# DECODED FIELDS
# ============================================================================

print("\n--- Decoded Fields ---")
print("\nIP Layer:")
print(f"  Version: {packet[IP].version}")
print(f"  Header Length: {packet[IP].ihl * 4} bytes (IHL={packet[IP].ihl})")
print(f"  Total Length: {packet[IP].len} bytes")
print(f"  TTL: {packet[IP].ttl}")
print(f"  Protocol: {packet[IP].proto} (TCP)")
print(f"  Source IP: {packet[IP].src} (0x{int.from_bytes(bytes(map(int, packet[IP].src.split('.'))), 'big'):08X})")
print(f"  Destination IP: {packet[IP].dst} (0x{int.from_bytes(bytes(map(int, packet[IP].dst.split('.'))), 'big'):08X})")
print(f"  Checksum: 0x{packet[IP].chksum:04X}")

print("\nTCP Layer:")
print(f"  Source Port: {packet[TCP].sport} (0x{packet[TCP].sport:04X})")
print(f"  Destination Port: {packet[TCP].dport} (0x{packet[TCP].dport:04X})")
print(f"  Sequence Number: {packet[TCP].seq} (0x{packet[TCP].seq:08X})")
print(f"  Acknowledgment: {packet[TCP].ack}")
print(f"  Data Offset: {packet[TCP].dataofs} ({packet[TCP].dataofs * 4} bytes)")
print(f"  Flags: {packet[TCP].flags} (SYN)")
print(f"  Window Size: {packet[TCP].window}")
print(f"  Checksum: 0x{packet[TCP].chksum:04X}")

# ============================================================================
# HEX DUMP
# ============================================================================

print("\n=== Complete Packet (Hex Dump) ===")
print(f"Total packet size: {len(packet)} bytes\n")

# Scapy's hexdump function shows the packet bytes
hexdump(packet)

# ============================================================================
# BYTE-BY-BYTE BREAKDOWN (educational)
# ============================================================================

print("\n--- Byte-by-Byte Breakdown ---")

# Convert packet to bytes
packet_bytes = bytes(packet)

print("IP Header (bytes 0-19):")
print(f"  Byte 0: 0x{packet_bytes[0]:02X} = Version {packet_bytes[0] >> 4}, IHL {packet_bytes[0] & 0x0F}")
print(f"  Bytes 2-3: 0x{packet_bytes[2]:02X}{packet_bytes[3]:02X} = Total length ({packet[IP].len} bytes)")
print(f"  Byte 8: 0x{packet_bytes[8]:02X} = TTL ({packet[IP].ttl})")
print(f"  Byte 9: 0x{packet_bytes[9]:02X} = Protocol ({packet[IP].proto} = TCP)")
print(f"  Bytes 12-15: Source IP ({packet[IP].src})")
print(f"  Bytes 16-19: Destination IP ({packet[IP].dst})")

print("\nTCP Header (bytes 20-39):")
print(f"  Bytes 20-21: 0x{packet_bytes[20]:02X}{packet_bytes[21]:02X} = Source port ({packet[TCP].sport})")
print(f"  Bytes 22-23: 0x{packet_bytes[22]:02X}{packet_bytes[23]:02X} = Dest port ({packet[TCP].dport})")
print(f"  Bytes 24-27: 0x{packet_bytes[24]:02X}{packet_bytes[25]:02X}{packet_bytes[26]:02X}{packet_bytes[27]:02X} = Sequence ({packet[TCP].seq})")
print(f"  Byte 33: 0x{packet_bytes[33]:02X} = Flags (SYN)")

# ============================================================================
# SEND PACKET
# ============================================================================

print("\n--- Sending Packet ---")

try:
    # send() sends at layer 3 (IP layer) - requires root
    # sendp() would send at layer 2 (Ethernet layer)
    send(packet, verbose=False)
    print(f"Packet sent successfully! ({len(packet)} bytes)")
    print("\nTo verify: run 'sudo tcpdump -i lo port 80' in another terminal")

except PermissionError:
    print("Send failed: Permission denied")
    print("\nHint: You need to run this with sudo")
    print("      sudo python3 same_in_scapy.py")
    sys.exit(1)

except Exception as e:
    print(f"Send failed: {e}")
    sys.exit(1)

# ============================================================================
# PROTOCOL REALITY CHECK
# ============================================================================

print("\n" + "=" * 70)
print("PROTOCOL REALITY CHECK")
print("=" * 70)
print("This 40-byte packet contains:")
print("  - 20-byte IP header (10 fields)")
print("  - 20-byte TCP header (10 fields)")
print("  - 0 bytes of data")
print("\nScapy constructed this in 3 lines of code.")
print("Manually, you'd need to:")
print("  1. Pack 20 fields into 40 bytes (correct byte order)")
print("  2. Calculate IP checksum over bytes 0-19")
print("  3. Calculate TCP checksum over pseudo-header + bytes 20-39")
print("\nProtocols = byte specifications. Scapy handles the tedium.")
print("=" * 70)


# ============================================================================
# FREQUENTLY ASKED QUESTIONS
# ============================================================================
#
# 1. Why do we need sudo/root to run this?
# -----------------------------------------
# Raw sockets allow you to construct packets from scratch, including
# the ability to forge source IP addresses. This is a security risk,
# so operating systems require elevated privileges (CAP_NET_RAW on Linux).
#
# Without sudo, you'll get: PermissionError: [Errno 1] Operation not permitted
#
#
# 2. What does the '/' operator do in IP(...)/TCP(...)?
# ------------------------------------------------------
# The '/' operator in Scapy means "layer on top of" or "encapsulate in".
# So IP(...)/TCP(...) means "TCP packet inside an IP packet".
#
# This matches the real network stack:
# - Application data goes inside TCP
# - TCP goes inside IP
# - IP goes inside Ethernet (at layer 2)
#
# You can chain multiple layers: Ether()/IP()/TCP()/Raw("data")
#
#
# 3. What's the difference between send() and sr1()?
# ---------------------------------------------------
# - send() = Send packet and don't wait for response ("fire and forget")
# - sr1() = Send packet and wait for 1 response (send and receive 1)
# - sr() = Send packet and capture all responses
#
# Use send() when you don't care about replies (like this example).
# Use sr1() when you need the response (like in ping or TCP handshake).
#
#
# 4. How does Scapy know what values to use for fields I didn't specify?
# -----------------------------------------------------------------------
# Scapy has sensible defaults for every field:
# - IP version = 4 (IPv4)
# - IP TTL = 64
# - IP protocol = automatically set based on upper layer (6 for TCP)
# - TCP window = 8192
# - TCP flags = None (empty)
#
# You can override ANY field: IP(ttl=1) or TCP(window=65535)
# Use packet.show() to see all field values (defaults + your overrides)
#
#
# 5. What's a checksum and why does it matter?
# ---------------------------------------------
# Checksums detect corruption during transmission. They're calculated
# by summing all bytes in a header, then taking the one's complement.
#
# If a single bit flips during transmission, the receiver recalculates
# the checksum and notices it doesn't match -> packet is corrupted.
#
# Scapy calculates checksums automatically. You can see them with:
#   packet.show()  # Shows checksums as 0x1234
#
# If you set a checksum manually, Scapy won't override it (useful for testing).
