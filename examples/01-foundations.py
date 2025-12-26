"""
Foundations: Protocol Building Blocks

Understanding the 4 layers of the TCP/IP model:
1. Application Layer (Layer 4) - HTTP, DNS, your data
2. Transport Layer (Layer 3) - TCP, UDP
3. Internet Layer (Layer 2) - IP
4. Link Layer (Layer 1) - Ethernet

Presented from familiar to unfamiliar.
"""

from scapy.all import IP, TCP, UDP, Ether, Raw, conf, hexdump  # type: ignore

conf.verb = 0


# Helper functions for consistent output formatting
def section_sep():
    """Print section separator (71 chars to match hexdump width)"""
    print("=" * 71)


def example_sep():
    """Print example separator (71 chars to match hexdump width)"""
    print("-" * 71)


# =======================================================================
# KEY CONCEPTS
# =======================================================================
# - Protocols are just structured bytes with agreed-upon field layouts
# - Each protocol layer has specific fields (addresses, ports, flags, etc.)
# - TCP/IP model has 4 layers: Link (1) -> Internet (2) -> Transport (3) -> Application (4)
# - Encapsulation order: Ether/IP/TCP/Raw (Layer 1 -> 2 -> 3 -> 4)
# - Higher layers (4) go INSIDE lower layers (1)
# - Checksums and header lengths are calculated automatically

section_sep()
print("FOUNDATIONS: THE 4 LAYERS OF TCP/IP")
section_sep()

print("\n┌─────────────────────────────────────────┐")
print("│  Application Layer                      │  HTTP, DNS, FTP")
print("│  (What applications use)                │")
print("├─────────────────────────────────────────┤")
print("│  Transport Layer                        │  TCP, UDP")
print("│  (Port-to-port communication)           │")
print("├─────────────────────────────────────────┤")
print("│  Internet Layer                         │  IP, ICMP")
print("│  (Host-to-host routing)                 │")
print("├─────────────────────────────────────────┤")
print("│  Link Layer                             │  Ethernet, ARP")
print("│  (Physical network access)              │")
print("└─────────────────────────────────────────┘")

print("\nNOTE: This breakdown is designed for web developers.")
print()
print("As a web developer, you work mostly with:")
print("  - Application Layer (HTTP, JSON, APIs)")
print("  - Transport Layer (TCP connections, ports)")
print()
print("That's why this guide has:")
print("  - Many examples for Application Layer (9 examples)")
print("  - Detailed TCP/UDP explanations with byte breakdowns")
print("  - Fewer examples for IP and Ethernet (you rarely need to touch these)")
print()
print("You don't need to understand every detail of IP routing or Ethernet")
print("frames to build web applications. But understanding how your HTTP")
print("requests become TCP segments helps you debug connection issues,")
print("understand timeouts, and reason about network performance.")

print("\nLearning path: Familiar (Layer 4) -> Unfamiliar (Layer 1)")
print("  Application -> Transport -> Internet -> Link")
section_sep()

# ============================================================================
# LAYER 4: APPLICATION DATA
# ============================================================================

print()
section_sep()
print("┌─────────────────────────────────────────┐")
print("│  Application Layer                      │  HTTP, DNS, FTP")
print("│  (What applications use)                │")
print("└─────────────────────────────────────────┘")
section_sep()

print("\nWhat is application data?")
print("- This is what you actually care about!")
print("- HTTP requests, JSON responses, emails, files, etc.")
print("- Just bytes that have meaning to your application")
print("- No headers, no protocol - just raw data")
print("- To lower layers (TCP, IP, Ethernet), it's all just bytes")

# --- Example 1: HTTP Request ---
print()
example_sep()
print("Example 1: HTTP Request")
example_sep()

http_request = Raw(
    load="GET /api/users HTTP/1.1\r\nHost: example.com\r\nUser-Agent: Python\r\n\r\n"
)

print("What: Web page/API request")
print(f"Size: {len(http_request)} bytes")
print("Content:")
print(f"  {repr(http_request.load)[2:-1]}")
print("\nHex Dump:")
_ = hexdump(http_request)

# --- Example 2: HTTP Response ---
print()
example_sep()
print("Example 2: HTTP Response")
example_sep()

http_response = Raw(
    load="HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body>Hello!</body></html>"
)

print("What: Server response to HTTP request")
print(f"Size: {len(http_response)} bytes")
print("Content:")
print(f"  {repr(http_response.load)[2:-1]}")
print("\nHex Dump:")
_ = hexdump(http_response)

# --- Example 3: JSON Data ---
print()
example_sep()
print("Example 3: JSON Data")
example_sep()

json_data = Raw(load='{"user": "alice", "age": 30, "active": true}')

print("What: API response data (structured)")
print(f"Size: {len(json_data)} bytes")
print("Content:")
print(f"  {repr(json_data.load)[2:-1]}")
print("\nHex Dump:")
_ = hexdump(json_data)

# --- Example 4: Plain Text ---
print()
example_sep()
print("Example 4: Plain Text Message")
example_sep()

plain_text = Raw(load="Hello, Network! This is a simple text message.")

print("What: Simple text message or file content")
print(f"Size: {len(plain_text)} bytes")
print("Content:")
print(f"  {repr(plain_text.load)[2:-1]}")
print("\nHex Dump:")
_ = hexdump(plain_text)

# --- Example 5: Email (SMTP) ---
print()
example_sep()
print("Example 5: Email Message")
example_sep()

email_data = Raw(
    load="From: alice@example.com\r\nTo: bob@example.com\r\nSubject: Hello\r\n\r\nHi Bob!"
)

print("What: Email message format (SMTP)")
print(f"Size: {len(email_data)} bytes")
print("Content:")
print(f"  {repr(email_data.load)[2:-1]}")
print("\nHex Dump:")
_ = hexdump(email_data)

# --- Example 6: DNS Query ---
print()
example_sep()
print("Example 6: DNS Query")
example_sep()

# DNS query for "example.com" A record
# This is simplified - real DNS has more fields
dns_query = Raw(
    load=b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01"
)

print("What: DNS query to resolve domain name to IP address")
print(f"Size: {len(dns_query)} bytes")
print("Content:")
print(f"  {repr(dns_query.load)[2:-1]}")
print("\nHex Dump:")
_ = hexdump(dns_query)
print("\nNotice: DNS queries are binary format, not text")
print("  - First 2 bytes: Transaction ID (0x1234)")
print("  - Contains domain name: 'example.com'")
print("  - Query type: A record (IPv4 address)")

# --- Example 7: FTP Commands ---
print()
example_sep()
print("Example 7: FTP Commands")
example_sep()

ftp_commands = Raw(load="USER alice\r\nPASS secret123\r\nLIST\r\nRETR document.pdf\r\n")

print("What: FTP protocol commands for file transfer")
print(f"Size: {len(ftp_commands)} bytes")
print("Content:")
print(f"  {repr(ftp_commands.load)[2:-1]}")
print("\nHex Dump:")
_ = hexdump(ftp_commands)
print("\nFTP commands:")
print("  - USER: authenticate with username")
print("  - PASS: provide password")
print("  - LIST: list files in directory")
print("  - RETR: retrieve (download) a file")

# --- Example 8: Binary Data (PNG Header) ---
print()
example_sep()
print("Example 8: Binary Data (PNG File Header)")
example_sep()

# PNG magic bytes: \x89PNG\r\n\x1a\n + IHDR chunk header
png_header = Raw(
    load=b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x00\x00\x00\x01\x00"
)

print("What: PNG image file header (binary data)")
print(f"Size: {len(png_header)} bytes")
print("Content:")
print(f"  {repr(png_header.load)[2:-1]}")
print("\nHex Dump:")
_ = hexdump(png_header)
print("\nNotice: Binary data looks different from text!")
print("  - First 4 bytes: \\x89PNG (PNG magic signature)")
print("  - Binary data is common for images, videos, executables")

# --- Example 9: Small File Content ---
print()
example_sep()
print("Example 9: CSV File Data")
example_sep()

csv_data = Raw(load="name,age,city\nAlice,30,NYC\nBob,25,SF\nCarol,35,LA")

print("What: CSV file content")
print(f"Size: {len(csv_data)} bytes")
print("Content:")
print(f"  {repr(csv_data.load)[2:-1]}")
print("\nHex Dump:")
_ = hexdump(csv_data)

print()
section_sep()
print("KEY INSIGHT: All of these are just bytes to TCP/IP/Ethernet!")
print("Lower layers don't care if it's HTTP, JSON, or a PNG file.")
print("They just transport the bytes from source to destination.")
section_sep()

# ============================================================================
# LAYER 3: TRANSPORT LAYER (TCP AND UDP)
# ============================================================================

print()
section_sep()
print("┌─────────────────────────────────────────┐")
print("│  Transport Layer                        │  TCP, UDP")
print("│  (Port-to-port communication)           │")
print("└─────────────────────────────────────────┘")
section_sep()

print("\nWhat is the Transport Layer?")
print("- Routes data to specific APPLICATIONS using port numbers")
print("- Two main protocols: TCP (reliable) and UDP (fast)")
print("- Ports identify which application: 80=HTTP, 53=DNS, 22=SSH, etc.")
print("- Source port (where it's from) + Destination port (where it's going)")

# =============================================================================
# TCP: Transmission Control Protocol
# =============================================================================

print()
section_sep()
print("TCP: TRANSMISSION CONTROL PROTOCOL")
section_sep()

print("\nWhat is TCP?")
print("- Reliable: guarantees delivery and correct order")
print("- Connection-oriented: establishes connection before sending data")
print("- Uses sequence numbers, acknowledgments, and retransmission")
print("- Slower than UDP, but ensures data integrity")
print("- Minimum 20 bytes header")

# --- Example 1: HTTP (Web Traffic) ---
print()
example_sep()
print("Example 1: TCP for HTTP (Web Traffic)")
example_sep()

tcp_http = TCP(
    sport=54321,  # Client port (random high port)
    dport=80,  # HTTP server port
    seq=1000,
    flags="S",  # SYN flag (connection request)
    window=65535,
)

print("What: Web browser requesting a page")
print(f"Size: {len(tcp_http)} bytes")
print("Key TCP Fields:")
print(f"  sport: {tcp_http.sport} (client's port)")
print(f"  dport: {tcp_http.dport} (HTTP server port)")
print(f"  seq: {tcp_http.seq} (sequence number for ordering)")
print(f"  flags: {tcp_http.flags} (SYN = connection request)")
print(f"  window: {tcp_http.window} (receive buffer size)")
print("\nHex Dump:")
_ = hexdump(tcp_http)

print("\nByte-by-Byte Breakdown:")
print("  Bytes 0-1:   D4 31        = Source port (0xD431 = 54321)")
print("  Bytes 2-3:   00 50        = Destination port (0x0050 = 80)")
print("  Bytes 4-7:   00 00 03 E8  = Sequence number (0x000003E8 = 1000)")
print("  Bytes 8-11:  00 00 00 00  = Acknowledgment number (0 = not used yet)")
print("  Byte 12:     50           = Data offset (0x5 = 5 words = 20 bytes)")
print("  Byte 13:     02           = Flags (0x02 = SYN)")
print("  Bytes 14-15: FF FF        = Window size (0xFFFF = 65535)")
print("  Bytes 16-17: XX XX        = Checksum (calculated automatically)")
print("  Bytes 18-19: 00 00        = Urgent pointer (0 = not used)")
print("\nNow you can see where 54321, 80, and 1000 are encoded!")

# --- Example 2: SYN-ACK (Server Response) ---
print()
example_sep()
print("Example 2: TCP SYN-ACK (Server Accepts Connection)")
example_sep()

tcp_synack = TCP(
    sport=80,  # Server's HTTP port
    dport=54321,  # Client's port
    seq=5000,  # Server's sequence number
    ack=1001,  # Acknowledging client's seq + 1
    flags="SA",  # SYN + ACK flags
    window=65535,
)

print("What: Server responding to client's connection request")
print(f"Size: {len(tcp_synack)} bytes")
print("Key TCP Fields:")
print(f"  sport: {tcp_synack.sport} (server's HTTP port)")
print(f"  dport: {tcp_synack.dport} (client's port)")
print(f"  seq: {tcp_synack.seq} (server's sequence number)")
print(f"  ack: {tcp_synack.ack} (acknowledging client's SYN)")
print(f"  flags: {tcp_synack.flags} (SA = SYN+ACK, accepting connection)")
print("\nHex Dump:")
_ = hexdump(tcp_synack)

print("\nByte-by-Byte Breakdown:")
print("  Bytes 0-1:   00 50        = Source port (0x0050 = 80)")
print("  Bytes 2-3:   D4 31        = Destination port (0xD431 = 54321)")
print("  Bytes 4-7:   00 00 13 88  = Sequence number (0x00001388 = 5000)")
print("  Bytes 8-11:  00 00 03 E9  = Acknowledgment number (0x000003E9 = 1001)")
print("  Byte 12:     50           = Data offset (20 bytes)")
print("  Byte 13:     12           = Flags (0x12 = SYN+ACK)")
print("  Bytes 14-15: FF FF        = Window size (65535)")
print("\nNotice: ack field is now used! Server acknowledges client's seq+1.")

# --- Example 3: ACK (Connection Established) ---
print()
example_sep()
print("Example 3: TCP ACK (Client Confirms Connection)")
example_sep()

tcp_ack = TCP(
    sport=54321,  # Client's port
    dport=80,  # Server's HTTP port
    seq=1001,  # Client's next sequence
    ack=5001,  # Acknowledging server's seq + 1
    flags="A",  # ACK flag only
    window=65535,
)

print("What: Client confirming connection is established")
print(f"Size: {len(tcp_ack)} bytes")
print("Key TCP Fields:")
print(f"  sport: {tcp_ack.sport} (client's port)")
print(f"  dport: {tcp_ack.dport} (server's HTTP port)")
print(f"  seq: {tcp_ack.seq} (client's next sequence)")
print(f"  ack: {tcp_ack.ack} (acknowledging server's SYN)")
print(f"  flags: {tcp_ack.flags} (A = ACK only, connection complete)")
print("\nHex Dump:")
_ = hexdump(tcp_ack)

print("\nAfter this packet, the TCP connection is established!")
print("This is the famous 'three-way handshake': SYN -> SYN-ACK -> ACK")

# --- Example 4: PSH-ACK (Sending Data) ---
print()
example_sep()
print("Example 4: TCP PSH-ACK (Sending Data)")
example_sep()

tcp_push = TCP(
    sport=54321,
    dport=80,
    seq=1001,
    ack=5001,
    flags="PA",  # PUSH + ACK flags
    window=65535,
)

print("What: Client sending HTTP request data to server")
print(f"Size: {len(tcp_push)} bytes")
print("Key TCP Fields:")
print(f"  sport: {tcp_push.sport} (client's port)")
print(f"  dport: {tcp_push.dport} (server's HTTP port)")
print(f"  seq: {tcp_push.seq} (sequence number for this data)")
print(f"  ack: {tcp_push.ack} (still acknowledging server)")
print(f"  flags: {tcp_push.flags} (PA = PUSH+ACK, sending data now!)")
print("\nHex Dump:")
_ = hexdump(tcp_push)

print("\nPUSH flag means: 'deliver this data to the application immediately'")
print("In real traffic, application data (HTTP request) would follow this header.")

# --- Example 5: FIN-ACK (Closing Connection) ---
print()
example_sep()
print("Example 5: TCP FIN-ACK (Closing Connection)")
example_sep()

tcp_fin = TCP(
    sport=54321,
    dport=80,
    seq=1501,  # After sending data
    ack=5001,
    flags="FA",  # FIN + ACK flags
    window=65535,
)

print("What: Client closing the connection gracefully")
print(f"Size: {len(tcp_fin)} bytes")
print("Key TCP Fields:")
print(f"  sport: {tcp_fin.sport} (client's port)")
print(f"  dport: {tcp_fin.dport} (server's HTTP port)")
print(f"  seq: {tcp_fin.seq} (after data was sent)")
print(f"  ack: {tcp_fin.ack} (acknowledging server)")
print(f"  flags: {tcp_fin.flags} (FA = FIN+ACK, closing connection)")
print("\nHex Dump:")
_ = hexdump(tcp_fin)

print("\nFIN flag means: 'I'm done sending data, close the connection'")
print("Server will respond with FIN-ACK, then client sends final ACK.")

# =============================================================================
# UDP: User Datagram Protocol
# =============================================================================

print()
section_sep()
print("UDP: USER DATAGRAM PROTOCOL")
section_sep()

print("\nWhat is UDP?")
print("- Fast: no connection setup, just send and forget")
print("- Unreliable: no guarantees of delivery or order")
print("- Connectionless: no handshake, no state tracking")
print("- Used when speed matters more than reliability")
print("- Only 8 bytes header (much smaller than TCP's 20 bytes)")

# --- Example 1: DNS (Domain Name Lookup) ---
print()
example_sep()
print("Example 1: UDP for DNS (Domain Name Lookup)")
example_sep()

udp_dns = UDP(
    sport=54326,
    dport=53,  # DNS server port
)

print("What: Looking up IP address for a domain name")
print(f"Size: {len(udp_dns)} bytes")
print("Key UDP Fields:")
print(f"  sport: {udp_dns.sport} (client's port)")
print(f"  dport: {udp_dns.dport} (DNS server port)")
print(f"  len: {udp_dns.len} (length of UDP header + data)")
print("\nHex Dump:")
_ = hexdump(udp_dns)

# --- Example 2: Video Streaming (RTP) ---
print()
example_sep()
print("Example 2: UDP for Video Streaming (RTP)")
example_sep()

udp_video = UDP(
    sport=54327,
    dport=5004,  # RTP (Real-time Transport Protocol) port
)

print("What: Streaming video/audio in real-time")
print(f"Size: {len(udp_video)} bytes")
print("Key UDP Fields:")
print(f"  sport: {udp_video.sport} (client's port)")
print(f"  dport: {udp_video.dport} (streaming server port)")
print(f"  len: {udp_video.len}")
print("\nWhy UDP for streaming?")
print("  - Speed is critical for real-time playback")
print("  - Losing a frame is OK, waiting for retransmission is NOT")
print("\nHex Dump:")
_ = hexdump(udp_video)

# --- Example 3: DHCP (IP Address Assignment) ---
print()
example_sep()
print("Example 3: UDP for DHCP (IP Address Assignment)")
example_sep()

udp_dhcp = UDP(
    sport=68,  # DHCP client port
    dport=67,  # DHCP server port
)

print("What: Requesting IP address from network")
print(f"Size: {len(udp_dhcp)} bytes")
print("Key UDP Fields:")
print(f"  sport: {udp_dhcp.sport} (DHCP client port)")
print(f"  dport: {udp_dhcp.dport} (DHCP server port)")
print(f"  len: {udp_dhcp.len}")
print("\nWhy UDP for DHCP?")
print("  - Client doesn't have an IP yet, can't establish TCP connection")
print("  - Needs to broadcast to find DHCP server")
print("\nHex Dump:")
_ = hexdump(udp_dhcp)

# --- Example 4: NTP (Time Synchronization) ---
print()
example_sep()
print("Example 4: UDP for NTP (Time Synchronization)")
example_sep()

udp_ntp = UDP(
    sport=54328,
    dport=123,  # NTP server port
)

print("What: Synchronizing system clock with time server")
print(f"Size: {len(udp_ntp)} bytes")
print("Key UDP Fields:")
print(f"  sport: {udp_ntp.sport} (client's port)")
print(f"  dport: {udp_ntp.dport} (NTP server port)")
print(f"  len: {udp_ntp.len}")
print("\nWhy UDP for NTP?")
print("  - Frequent small queries, connection overhead not worth it")
print("  - Can retry if packet lost")
print("\nHex Dump:")
_ = hexdump(udp_ntp)

print()
section_sep()
print("TCP vs UDP: Key Differences")
section_sep()
print("\nTCP (Transmission Control Protocol):")
print("  + Reliable delivery (guaranteed)")
print("  + Ordered packets (arrives in correct order)")
print("  + Connection-oriented (handshake required)")
print("  - Slower (overhead from reliability mechanisms)")
print("  Use for: Web, email, file transfer, SSH")
print()
print("UDP (User Datagram Protocol):")
print("  + Fast (no connection setup)")
print("  + Low overhead (8-byte header vs TCP's 20 bytes)")
print("  - Unreliable (packets can be lost)")
print("  - No ordering (packets can arrive out of order)")
print("  Use for: DNS, streaming, gaming, VoIP")
section_sep()

print()
section_sep()
print("KEY INSIGHT: Lower layers don't care about TCP vs UDP!")
section_sep()
print("\nJust like IP and Ethernet don't care if you're sending HTTP or JSON,")
print("they ALSO don't care if you're using TCP or UDP.")
print()
print("To the IP layer:")
print("  - TCP segment = just bytes to put in the IP payload")
print("  - UDP datagram = just bytes to put in the IP payload")
print()
print("IP has a 'protocol' field that says what's inside:")
print("  - Protocol 6 = TCP")
print("  - Protocol 17 = UDP")
print("  - Protocol 1 = ICMP")
print()
print("But IP doesn't understand or process TCP/UDP headers.")
print("It just delivers the bytes to the right host.")
print()
print("Same for Ethernet:")
print("  - Doesn't care about TCP, UDP, or even IP")
print("  - Just sees bytes and delivers to MAC address")
print("  - Has 'type' field: 0x0800 = IPv4 inside")
print()
print("Each layer treats higher layers as 'application data':")
print("  - To TCP/UDP: HTTP is just application data")
print("  - To IP: TCP/UDP segments are just transport data")
print("  - To Ethernet: IP packets are just network data")
section_sep()

# ============================================================================
# LAYER 2: IP PACKET
# ============================================================================

print()
section_sep()
print("┌─────────────────────────────────────────┐")
print("│  Internet Layer                         │  IP, ICMP")
print("│  (Host-to-host routing)                 │")
print("└─────────────────────────────────────────┘")
section_sep()

ip_packet = IP(
    version=4,  # IPv4
    ttl=64,  # Time to Live: 64 hops
    src="192.168.1.100",  # Source IP
    dst="8.8.8.8",  # Destination IP (Google DNS)
)

print("\nWhat is an IP packet?")
print("- Internet layer protocol")
print("- Routes packets between hosts across DIFFERENT networks")
print("- Contains source and destination IP ADDRESSES")
print("- IP addresses identify which host (computer) on the internet")
print("- Minimum 20 bytes (can be larger with options)")

print("\nIP Packet Structure:")
_ = ip_packet.show()

print("\nKey IP Fields:")
print(f"  version: {ip_packet.version} (IPv4 or IPv6)")
print(f"  ttl: {ip_packet.ttl} (hops before packet is discarded)")
print(f"  proto: {ip_packet.proto} (what's inside: TCP=6, UDP=17, ICMP=1)")
print(f"  src: {ip_packet.src} (source IP address - who is sending)")
print(f"  dst: {ip_packet.dst} (destination IP address - who receives)")

print("\nHex Dump:")
_ = hexdump(ip_packet)

# ============================================================================
# LAYER 1: ETHERNET FRAME
# ============================================================================

print()
section_sep()
print("┌─────────────────────────────────────────┐")
print("│  Link Layer                             │  Ethernet, ARP")
print("│  (Physical network access)              │")
print("└─────────────────────────────────────────┘")
section_sep()

ether_frame = Ether(
    src="aa:bb:cc:dd:ee:ff",  # Source MAC address
    dst="11:22:33:44:55:66",  # Destination MAC address
    type=0x0800,  # EtherType: 0x0800 = IPv4
)

print("\nWhat is an Ethernet frame?")
print("- Link layer protocol")
print("- Transfers data between devices on the SAME network (local)")
print("- Contains source and destination MAC ADDRESSES")
print("- MAC addresses identify network interface cards (hardware)")
print("- 14 bytes header (6 bytes dst MAC + 6 bytes src MAC + 2 bytes type)")

print("\nEthernet Frame Structure:")
_ = ether_frame.show()

print("\nKey Ethernet Fields:")
print(f"  dst: {ether_frame.dst} (destination MAC address)")
print(f"  src: {ether_frame.src} (source MAC address)")
print(f"  type: 0x{ether_frame.type:04X} (what's inside: 0x0800=IPv4, 0x0806=ARP)")

print("\nHex Dump:")
_ = hexdump(ether_frame)

print("\nWhy MAC addresses?")
print("  - MAC = Media Access Control address (hardware address)")
print("  - Every network card has a unique MAC address")
print("  - Used for local delivery (within same network/LAN)")
print("  - Different from IP (which is for routing across networks)")

# ============================================================================
# PUTTING IT ALL TOGETHER: 4-LAYER PACKET
# ============================================================================

print()
section_sep()
print("PUTTING IT ALL TOGETHER: 4 LAYERS IN ONE PACKET")
section_sep()

print("\nNow let's build a COMPLETE packet with all 4 layers:")
print("  Layer 4: HTTP GET request (application data)")
print("  Layer 3: TCP segment (transport)")
print("  Layer 2: IP packet (internet)")
print("  Layer 1: Ethernet frame (link)")
print()
print("This is what actually travels on the network when you visit a website!")

# Build realistic HTTP GET request with all 4 layers
full_packet = (
    Ether(
        src="aa:bb:cc:11:22:33",  # Client's MAC address
        dst="ff:ee:dd:44:55:66",  # Router's MAC address
        type=0x0800,  # IPv4
    )
    / IP(
        version=4,
        ttl=64,
        src="192.168.1.100",  # Client's IP
        dst="93.184.216.34",  # example.com's IP
        proto=6,  # TCP
    )
    / TCP(
        sport=54321,  # Client's ephemeral port
        dport=80,  # HTTP port
        flags="PA",  # PUSH-ACK (sending data)
        seq=1000,
        ack=5000,
        window=65535,
    )
    / Raw(load="GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
)

print()
example_sep()
print("Complete 4-Layer Packet")
example_sep()

print(f"\nTotal packet size: {len(full_packet)} bytes")
print("  Layer 1 (Ethernet): 14 bytes header")
print("  Layer 2 (IP):       20 bytes header")
print("  Layer 3 (TCP):      20 bytes header")
print("  Layer 4 (HTTP):     41 bytes data")
print()

print("Full Packet Hex Dump:")
_ = hexdump(full_packet)

print()
print("Key bytes breakdown:")
print("-" * 71)
print("Bytes 0-13:   Ethernet header")
print("              [0-5]   dst MAC: ff:ee:dd:44:55:66")
print("              [6-11]  src MAC: aa:bb:cc:11:22:33")
print("              [12-13] type: 0x0800 (IPv4)")
print()
print("Bytes 14-33:  IP header")
print("              [14]    version + header length: 4 + 5 words")
print("              [22]    TTL: 64")
print("              [23]    protocol: 6 (TCP)")
print("              [26-29] src IP: 192.168.1.100")
print("              [30-33] dst IP: 93.184.216.34")
print()
print("Bytes 34-53:  TCP header")
print("              [34-35] src port: 54321")
print("              [36-37] dst port: 80")
print("              [38-41] sequence: 1000")
print("              [42-45] acknowledgment: 5000")
print("              [47]    flags: 0x18 (PUSH + ACK)")
print()
print("Bytes 54+:    HTTP data (readable text)")
print("              'GET / HTTP/1.1\\r\\nHost: example.com\\r\\n\\r\\n'")
print("-" * 71)

print()
print("Encapsulation visualization:")
print()
print("┌─────────────────────────────────────────────────────────────────┐")
print("│ Ethernet Header                                                 │")
print("│ ┌───────────────────────────────────────────────────────────┐   │")
print("│ │ IP Header                                                 │   │")
print("│ │ ┌─────────────────────────────────────────────────────┐   │   │")
print("│ │ │ TCP Header                                          │   │   │")
print("│ │ │ ┌───────────────────────────────────────────────┐   │   │   │")
print("│ │ │ │ HTTP Data: 'GET / HTTP/1.1\\r\\n...'            │   │   │   │")
print("│ │ │ └───────────────────────────────────────────────┘   │   │   │")
print("│ │ └─────────────────────────────────────────────────────┘   │   │")
print("│ └───────────────────────────────────────────────────────────┘   │")
print("└─────────────────────────────────────────────────────────────────┘")
print()
print("Each layer wraps the previous:")
print("  - Ethernet sees everything else as 'payload'")
print("  - IP sees TCP+HTTP as 'payload'")
print("  - TCP sees HTTP as 'payload'")
print("  - HTTP is the actual application data")
print()
print("When this packet travels:")
print("  1. Network card reads Ethernet header -> knows it's for this machine")
print("  2. Operating system reads IP header -> knows which host to deliver to")
print("  3. Operating system reads TCP header -> knows which port/application")
print("  4. Application reads HTTP data -> processes the web request")
print()
print("Each layer strips its header and passes data up the stack!")

# Add spacing before FAQ
print("\n\n\n\n")

# ============================================================================
# PRINTED FAQ (for program output / website)
# ============================================================================

section_sep()
print("FREQUENTLY ASKED QUESTIONS")
section_sep()

print(
    "\nQ: What exactly IS HTTP? Is it just the syntax like 'GET /api/users HTTP/1.1'?"
)
example_sep()
print("""
YES! HTTP (HyperText Transfer Protocol) IS that text syntax you see.

HTTP is an application-layer protocol that defines a specific text format for
requests and responses between web clients (browsers) and servers.

What you see in the hex dump:
  'GET /api/users HTTP/1.1\\r\\nHost: example.com\\r\\n\\r\\n'

...IS the actual HTTP protocol. Those bytes ARE HTTP.

HTTP defines:
  - Request format: METHOD PATH VERSION\\r\\n
    - GET, POST, PUT, DELETE (methods)
    - /api/users (path/resource)
    - HTTP/1.1 (version)

  - Headers: Key: Value\\r\\n
    - Host: example.com
    - Content-Type: application/json
    - User-Agent: Mozilla/5.0

  - Body separator: \\r\\n\\r\\n (blank line)

  - Response format: VERSION STATUS MESSAGE\\r\\n
    - HTTP/1.1 200 OK
    - HTTP/1.1 404 Not Found

HTTP is NOT:
  - A programming language
  - HTML (that's the content format inside HTTP)
  - The web browser (that's the client that uses HTTP)
  - A separate thing from the text - the text IS the protocol

Think of it this way:
  Protocol = Agreement about byte format
  HTTP = Agreement to use "GET /path HTTP/1.1\\r\\n..." format

When you see those bytes on the wire, you're seeing HTTP in action.
No magic, no abstraction - just text formatted according to the rules.

Other text-based protocols work the same way:
  - SMTP (email): "MAIL FROM:<alice@example.com>\\r\\n"
  - FTP (files): "USER alice\\r\\n"
  - POP3 (email): "RETR 1\\r\\n"

Some protocols use binary format instead of text:
  - DNS: Binary format with length prefixes
  - Most of this is for efficiency (binary is more compact than text)
""")

print("\nQ: Do all packets need all 4 layers? What combinations are valid?")
example_sep()
print("""
NO! Not all data needs all 4 layers. It depends on what you're doing.

Valid combinations:

1. Ethernet only (Layer 1):
   [Ethernet Header] [Data] [Ethernet Trailer]
   Example: ARP (Address Resolution Protocol)
   - Used to find MAC address for an IP address
   - Stays on local network, never goes beyond router

2. Ethernet + IP (Layers 1 + 2):
   [Ethernet Header] [IP Header] [Data] [Ethernet Trailer]
   Example: ICMP ping
   - Can travel across networks (routers)
   - No port numbers (no TCP/UDP needed)

3. Ethernet + IP + TCP (Layers 1 + 2 + 3):
   [Ethernet Header] [IP Header] [TCP Header] [Data] [Ethernet Trailer]
   Example: Empty TCP ACK (connection establishment)
   - Has ports, but no application data yet

4. Ethernet + IP + TCP/UDP + Application Data (All 4 layers):
   [Ethernet Header] [IP Header] [TCP Header] [HTTP Request] [Ethernet Trailer]
   Example: Web request, email, file transfer
   - This is the most common for internet traffic

5. Loopback (no Ethernet at all!):
   [IP Header] [TCP Header] [Data]
   Example: Connecting to localhost (127.0.0.1)
   - Data never leaves your computer
   - No need for Ethernet (no physical network)

The layers you need depend on:
  - Where you're sending (local network vs internet)
  - What you're doing (connection management vs data transfer)
  - Physical medium (wired, wireless, loopback)

Most web traffic you see is: Ethernet + IP + TCP + HTTP
But not everything needs all layers!
""")

print("\nQ: Who adds these headers? My server? The router? The OS?")
example_sep()
print("""
Your APPLICATION and OPERATING SYSTEM add headers. Routers just forward.

Here's the journey when you send an HTTP request:

1. YOUR APPLICATION (web server, browser):
   Creates: [HTTP Request]
   Example: "GET /api/users HTTP/1.1\\r\\n..."

2. OPERATING SYSTEM - Transport Layer (TCP/UDP):
   Adds TCP/UDP header with port numbers:
   [TCP Header: sport=54321, dport=80, seq=1000...] [HTTP Request]

3. OPERATING SYSTEM - Network Layer (IP):
   Adds IP header with addresses:
   [IP Header: src=192.168.1.100, dst=93.184.216.34...] [TCP Header] [HTTP Request]

4. NETWORK CARD DRIVER - Link Layer (Ethernet):
   Adds Ethernet header and trailer:
   [Ethernet Header: src=AA:BB:CC, dst=11:22:33...] [IP] [TCP] [HTTP] [CRC Checksum]

Your server does NOT add headers manually!
The operating system's network stack does it automatically when you:
  - Call socket.send() in Python
  - Use fetch() in JavaScript
  - Make any network request

What about ROUTERS?
  - Router receives: [Ethernet] [IP] [TCP] [HTTP] [CRC]
  - Router strips Ethernet header (checks destination MAC)
  - Router looks at IP header (checks destination IP)
  - Router adds NEW Ethernet header for next hop
  - Router forwards: [New Ethernet] [IP] [TCP] [HTTP] [New CRC]

Each device only processes layers it needs:
  - Your app: Layer 4 (HTTP)
  - Your OS: Layers 3 + 2 (TCP + IP)
  - Your network card: Layer 1 (Ethernet)
  - Router: Strips Layer 1, reads Layer 2, adds new Layer 1
  - Destination: Strips each layer from outside-in
""")

print("\nQ: Are they called 'headers'? Do they have 'trailers' too?")
example_sep()
print("""
YES, they're called HEADERS. Some layers also have TRAILERS.

Header = Data at the BEGINNING
Trailer = Data at the END

Which layers have what:

TCP: Header only (20 bytes minimum)
  [TCP Header: ports, seq, flags, etc.] [Data]

UDP: Header only (8 bytes)
  [UDP Header: ports, length, checksum] [Data]

IP: Header only (20 bytes minimum)
  [IP Header: addresses, TTL, protocol, etc.] [Data]

Ethernet: Header AND Trailer
  [Ethernet Header: 14 bytes] [Data] [Ethernet Trailer: 4 bytes CRC]
  - Trailer is a checksum (CRC) to detect corruption
  - Only Ethernet has a trailer in the TCP/IP model

Complete packet structure:
┌─────────────┬────────────┬────────────┬──────────┬─────────────┐
│   Ethernet  │  IP Header │ TCP Header │   HTTP   │  Ethernet   │
│   Header    │  20 bytes  │  20 bytes  │  Request │   Trailer   │
│   14 bytes  │            │            │          │   4 bytes   │
└─────────────┴────────────┴────────────┴──────────┴─────────────┘
     Header      Header       Header       Data        Trailer

Why do we say "wrap"?
Because each layer ENCAPSULATES (wraps) the layer above it:
  1. Start with HTTP request: [HTTP]
  2. TCP wraps it: [TCP Header][HTTP]
  3. IP wraps that: [IP Header][TCP Header][HTTP]
  4. Ethernet wraps all: [Eth Header][IP][TCP][HTTP][Eth Trailer]

When receiving, we UNWRAP from outside to inside:
  1. Strip Ethernet: [IP][TCP][HTTP]
  2. Strip IP: [TCP][HTTP]
  3. Strip TCP: [HTTP]
  4. Application reads: HTTP request
""")

print("\nQ: Which devices/software need which layers?")
example_sep()
print("""
Each device only processes the layers it needs. Let's trace a web request.

YOUR COMPUTER (sending HTTP request):

  - Web Browser (Application):
    - Creates HTTP request: "GET /index.html HTTP/1.1..."
    - Passes to OS: "Send this to example.com port 80"
    - Needs: Layer 4 only

  - Operating System (Network Stack):
    - Adds TCP header: sport, dport, seq, flags, etc.
    - Adds IP header: source IP, destination IP, TTL, etc.
    - Needs: Layers 3 + 2

  - Network Card Driver:
    - Adds Ethernet header: source MAC, destination MAC
    - Sends actual electrical signals on wire
    - Needs: Layer 1

YOUR ROUTER:

  - Receives: [Ethernet][IP][TCP][HTTP][CRC]
  - Strips Ethernet header (was for router's MAC address)
  - Reads IP header: "This goes to 93.184.216.34"
  - Looks up routing table: "Send via ISP gateway"
  - Adds NEW Ethernet header for next hop
  - Forwards: [New Ethernet][IP][TCP][HTTP][New CRC]
  - Needs: Layers 1 + 2 (Ethernet + IP)
  - Does NOT look at TCP or HTTP!

INTERMEDIATE ROUTERS (on the internet):

  - Same as your router
  - Strip Ethernet, read IP, add new Ethernet
  - Each hop changes Ethernet header
  - IP header stays mostly the same (except TTL decrements)
  - Needs: Layers 1 + 2

DESTINATION SERVER (example.com):

  - Network Card:
    - Receives electrical signals
    - Strips Ethernet header and trailer
    - Passes to OS: [IP][TCP][HTTP]

  - Operating System:
    - Strips IP header: "This is for me (my IP address)"
    - Strips TCP header: "Port 80 = web server"
    - Passes to application: [HTTP]

  - Web Server (nginx, Apache, Node.js):
    - Receives HTTP request
    - Processes: "GET /index.html"
    - Sends response back (same process in reverse)

KEY INSIGHT:
  - Applications: Only see Layer 4 (HTTP, FTP, etc.)
  - Operating Systems: Handle Layers 3 + 2 (TCP/UDP + IP)
  - Network Cards: Handle Layer 1 (Ethernet)
  - Routers: Only look at Layers 1 + 2 (Ethernet + IP)

Each layer strips its header and passes up:
  Ethernet -> IP -> TCP -> Application
  (outside)              (inside)

This is why it's called "encapsulation" - each layer wraps the previous.
""")

print("\nQ: Why TCP handshake? Does every HTTP request need a separate handshake?")
example_sep()
print("""
NO! The TCP handshake happens ONCE per connection, not per request.

Here's how it works:

1. TCP Handshake (happens ONCE):
   Client -> Server: SYN
   Server -> Client: SYN-ACK
   Client -> Server: ACK
   [Connection is now OPEN and stays open]

2. Send many HTTP requests (reusing the same connection):
   Client -> Server: HTTP Request 1
   Server -> Client: HTTP Response 1
   Client -> Server: HTTP Request 2
   Server -> Client: HTTP Response 2
   Client -> Server: HTTP Request 3
   Server -> Client: HTTP Response 3
   [All use the SAME TCP connection, no new handshake]

3. Close connection (when done):
   Client -> Server: FIN-ACK
   Server -> Client: FIN-ACK
   [Connection is now CLOSED]

Why establish a connection if data can still get corrupted?

The handshake establishes:
  - Initial sequence numbers (where to start counting)
  - Window sizes (how much data can be sent at once)
  - Both sides agree the connection exists

After handshake, TCP handles corruption with:
  - Checksums: Detect corrupted packets
  - Sequence numbers: Detect missing or out-of-order packets
  - Acknowledgments: Confirm "I received packet X"
  - Retransmission: Resend if packet lost or corrupted

Example of corruption handling:
  Client sends: seq=1000, data=[100 bytes]
  Server receives: Checksum fails (corrupted!)
  Server ignores corrupted packet
  Server doesn't send ACK for seq=1000
  Client waits... timeout... retransmits seq=1000
  Server receives good copy, sends ACK=1100

The handshake is for CONNECTION setup.
Checksums/sequence numbers/ACKs are for DATA reliability.

HTTP/1.1 persistent connections:
  - One TCP connection can handle many HTTP requests
  - Header: "Connection: keep-alive" (default in HTTP/1.1)
  - Faster: No handshake overhead for each request
  - Browser typically keeps connection open for 60-120 seconds

So a typical web page load:
  1. TCP handshake (once)
  2. HTTP request for HTML (uses that connection)
  3. HTTP request for CSS (reuses same connection)
  4. HTTP request for JS (reuses same connection)
  5. HTTP request for images (reuses same connection)
  6. Connection closes after idle timeout

Only ONE handshake for dozens of HTTP requests!
""")

section_sep()
