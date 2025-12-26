"""
TLS and HTTPS: Encrypted Communication

Understanding how HTTPS protects HTTP traffic using TLS encryption.

This demonstrates:
- Difference between HTTP (plaintext) and HTTPS (encrypted)
- TLS handshake process
- What encryption actually looks like in packets
"""

from scapy.all import Raw, TCP, conf, hexdump  # type: ignore
from scapy.layers.tls.handshake import TLSClientHello  # type: ignore
from scapy.layers.tls.record import TLS  # type: ignore

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
# - HTTP sends data in plaintext (readable by anyone)
# - HTTPS = HTTP + TLS encryption (unreadable without decryption key)
# - TLS (Transport Layer Security) encrypts data BEFORE it goes into TCP
# - TLS handshake establishes encryption keys between client and server
# - Only encrypted payload travels on the network
# - Encryption prevents eavesdropping and tampering

section_sep()
print("TLS AND HTTPS: WHY ENCRYPTION MATTERS")
section_sep()

print("\n                    WITHOUT TLS (HTTP)")
print("┌──────────┐                              ┌──────────┐")
print("│          │  GET /login?password=secret  │          │")
print("│  Client  │ ───────────────────────────> │  Server  │")
print("│          │     (plaintext, readable)    │          │")
print("└──────────┘                              └──────────┘")
print("      ↑")
print("      └─────── Anyone on the network can read this!")
print()
print("                     WITH TLS (HTTPS)")
print("┌──────────┐                              ┌──────────┐")
print("│          │  [encrypted gibberish]       │          │")
print("│  Client  │ ───────────────────────────> │  Server  │")
print("│          │     (only server can read)   │          │")
print("└──────────┘                              └──────────┘")
print()
print("TLS encrypts your data so only the intended recipient can read it.")
print("Even if someone intercepts the packet, they see random bytes.")
section_sep()

# ============================================================================
# WHERE DOES TLS FIT IN THE LAYER MODEL?
# ============================================================================

print()
section_sep()
print("WHERE DOES TLS FIT IN THE TCP/IP MODEL?")
section_sep()

print("\nTLS sits BETWEEN the Transport Layer (TCP) and Application Layer (HTTP):")
print()
print("Without TLS (plain HTTP):")
print("  [Ethernet] [IP] [TCP port 80] [HTTP Request - readable]")
print()
print("With TLS (HTTPS):")
print("  [Ethernet] [IP] [TCP port 443] [TLS: Encrypted HTTP - unreadable]")
print()
print("Key points:")
print("  - TLS encrypts the application data BEFORE it goes into TCP")
print("  - Different port numbers (80 vs 443) tell the server what to expect")
print("  - Port 80:  Server expects plain HTTP immediately")
print("  - Port 443: Server expects TLS handshake first, then encrypted HTTP")
print()
print("Why different ports?")
print("  - The server needs to know whether to start with TLS handshake or not")
print("  - Port 80:  Client sends HTTP directly")
print("  - Port 443: Client sends TLS messages first to set up encryption")
print("  - It's like calling a regular phone (80) vs. a secure line (443)")
print()
print("What is 'ClientHello' and 'ServerHello'?")
print("  ClientHello = First TLS message from client to server")
print("    - Says: 'I want to use TLS, here are the encryption methods I support'")
print("    - Contains: List of cipher suites, TLS version, random number")
print("    - This is APPLICATION DATA inside a TCP packet, not a TCP flag")
print()
print("  ServerHello = Second TLS message from server to client")
print("    - Says: 'OK, let's use THIS specific encryption method'")
print("    - Contains: Chosen cipher suite, TLS version, random number")
print("    - Also APPLICATION DATA inside a TCP packet")
print()
print("  These are NOT like SYN/ACK (which are TCP flags).")
print("  They are actual DATA messages with structure and fields.")
print()
print("TLS wraps HTTP, then TCP wraps TLS:")
print("  1. Take HTTP request: 'GET /login?password=...'")
print("  2. Encrypt it with TLS: [random-looking bytes]")
print("  3. Put it in TCP packet to port 443")
print("  4. Send over network")
section_sep()

# ============================================================================
# DEMO 1: PLAIN HTTP REQUEST (READABLE)
# ============================================================================

print()
section_sep()
print("DEMO 1: HTTP WITHOUT ENCRYPTION (PLAINTEXT)")
section_sep()

print("\nLet's build a complete HTTP packet (TCP + HTTP):")
print()

# Build complete packet with TCP + HTTP
http_packet_plain = (
    TCP(
        sport=54321,  # Client's port
        dport=80,  # HTTP port (unencrypted)
        flags="PA",  # PUSH-ACK (sending data)
        seq=1000,
        ack=5000,
    )
    / Raw(load="GET /account?password=MySecret123 HTTP/1.1\r\nHost: bank.com\r\n\r\n")
)

print("Packet structure:")
print("  [TCP Header: sport=54321, dport=80] [HTTP Request]")
print()
print(f"Total size: {len(http_packet_plain)} bytes")
print("  TCP header:  20 bytes")
print("  HTTP data:   62 bytes")
print()

print("Full Packet Hex Dump:")
_ = hexdump(http_packet_plain)

print("\nNotice: You can READ the password in the hex dump!")
print("Look at the ASCII column on the right -> 'password=MySecret123'")
print()
print("The packet structure shows:")
print("  - Bytes 0-19:  TCP header (port 80 visible)")
print("  - Bytes 20+:   HTTP request (completely readable)")
print()
print("Anyone with a packet sniffer (Wireshark, tcpdump) can see:")
print("  - The URL you're visiting")
print("  - Passwords and credentials")
print("  - Cookies and session tokens")
print("  - Personal information")
print()
print("This is why HTTP is dangerous for sensitive data.")

# ============================================================================
# DEMO 2: HTTPS/TLS REQUEST (ENCRYPTED)
# ============================================================================

print()
section_sep()
print("DEMO 2: HTTPS WITH ENCRYPTION (UNREADABLE)")
section_sep()

print("\nHOW does the data get encrypted?")
print()
print("The encryption process:")
print("  1. TCP handshake completes (SYN, SYN-ACK, ACK)")
print("  2. TLS handshake completes (ClientHello, ServerHello, etc.)")
print("  3. Both sides now have shared encryption keys")
print("  4. Client takes HTTP request: 'GET /account?password=MySecret123...'")
print("  5. Client encrypts it using the TLS session key")
print("  6. Client wraps encrypted data in TLS record header")
print("  7. Client puts TLS record in TCP packet to port 443")
print("  8. Server receives, decrypts using the same key")
print()
print("Let's see what this looks like on the wire:")
print()

# Simulate encrypted payload (in real TLS, this would be actual encrypted bytes)
# This represents the SAME HTTP request as Demo 1, but encrypted
encrypted_payload = bytes.fromhex(
    "17 03 03 00 40 "  # TLS record header: Type=23 (Application Data), Version=TLS 1.2, Length=64
    + "d4 7f 3a 91 c8 25 6f 4e b2 11 83 9d 47 2c 6a 15 "  # Encrypted data (was: GET /account...)
    + "8f 9a 2d 73 11 6c 84 9f 3d 4a 71 5e 88 b3 21 09 "  # More encrypted data
    + "6d 4f 82 7a 93 1c 5f 68 a4 0f 97 2b 44 1d 89 73 "  # More encrypted data
    + "f5 8c 61 3e 29 94 b7 6f 11 c5 82 3a 67 94 1f 28 "  # End of encrypted data
)

# Build complete HTTPS packet (TCP + TLS encrypted data)
https_packet_encrypted = (
    TCP(
        sport=54321,  # Client's port
        dport=443,  # HTTPS port (encrypted)
        flags="PA",  # PUSH-ACK (sending data)
        seq=2000,
        ack=6000,
    )
    / Raw(load=encrypted_payload)
)

print("Packet structure:")
print("  [TCP Header: sport=54321, dport=443] [TLS: Encrypted HTTP]")
print()
print(f"Total size: {len(https_packet_encrypted)} bytes")
print("  TCP header:       20 bytes")
print("  TLS record:       69 bytes")
print("    - TLS header:    5 bytes (type, version, length)")
print("    - Encrypted data: 64 bytes (the HTTP request, encrypted)")
print()

print("Full Packet Hex Dump:")
_ = hexdump(https_packet_encrypted)

print("\nNotice: Complete gibberish after the TCP header!")
print("The ASCII column shows no readable text.")
print()
print("Compare with Demo 1:")
print("  Demo 1 (HTTP):  Port 80,  readable 'GET /account?password=...'")
print("  Demo 2 (HTTPS): Port 443, random bytes")
print()
print("The packet structure shows:")
print("  - Bytes 0-19:  TCP header (port 443 visible)")
print("  - Bytes 20-24: TLS record header (type=0x17, version=0x0303)")
print("  - Bytes 25+:   Encrypted data (unreadable gibberish)")
print()
print("This encrypted blob contains the SAME HTTP request:")
print("  - Original: 'GET /account?password=MySecret123...'")
print("  - Encrypted using the TLS session key (established in handshake)")
print("  - Only the server (with the matching decryption key) can read it")
print()
print("An attacker sees random bytes and cannot:")
print("  - Read the URL")
print("  - See passwords")
print("  - Extract cookies")
print("  - Understand anything")
print()
print("The encryption key is unique for this session and was established")
print("during the TLS handshake (which we'll see in Demo 3).")

# ============================================================================
# DEMO 3: TLS HANDSHAKE STRUCTURE
# ============================================================================

print()
section_sep()
print("DEMO 3: TLS HANDSHAKE - HOW ENCRYPTION IS ESTABLISHED")
section_sep()

print("\nIMPORTANT: TLS handshake is DIFFERENT from TCP handshake!")
print()
print("There are TWO handshakes when you connect to an HTTPS website:")
print()
print("1. TCP Handshake (Layer 3 - Transport Layer):")
print("   Client -> Server: SYN")
print("   Server -> Client: SYN-ACK")
print("   Client -> Server: ACK")
print("   Result: TCP connection established")
print()
print("2. TLS Handshake (Layer 4 - Application Layer):")
print("   Client -> Server: ClientHello")
print("   Server -> Client: ServerHello")
print("   [More messages...]")
print("   Result: Encryption keys established")
print()
print("Key differences:")
print("  TCP handshake:")
print("    - Uses TCP flags (SYN, ACK)")
print("    - Establishes connection (can we talk?)")
print("    - No encryption yet")
print()
print("  TLS handshake:")
print("    - Uses application data (ClientHello, ServerHello)")
print("    - These are DATA inside TCP packets, not TCP flags")
print("    - Establishes encryption (how do we encrypt?)")
print("    - Happens AFTER TCP connection exists")
print()
print("Think of it:")
print("  TCP handshake = Opening a phone line")
print("  TLS handshake = Agreeing on a secret code to speak in")
print()
section_sep()

print("\nNow, let's look at the TLS handshake in detail:")
print()
print("Before any encrypted data flows, client and server perform")
print("the TLS HANDSHAKE to agree on encryption keys.")
print()
print("TLS Handshake steps:")
print("  1. ClientHello  -> Client: 'I want to use TLS, here are my options'")
print("  2. ServerHello  -> Server: 'OK, let's use these encryption methods'")
print("  3. Certificate  -> Server: 'Here's my identity proof (certificate)'")
print("  4. Key Exchange -> Both: 'Let's agree on a secret encryption key'")
print("  5. Finished     -> Both: 'Handshake complete, let's start encrypting!'")
print()
print("After TLS handshake completes, all HTTP data is encrypted.")
print("(The TCP connection stays open for the entire time.)")

print()
example_sep()
print("Example: TLS ClientHello (Step 1)")
example_sep()

# Build a minimal TLS ClientHello
client_hello = TLS(
    msg=[
        TLSClientHello(
            version=0x0303,  # TLS 1.2
            ciphers=[
                0xC02F,  # TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
                0xC030,  # TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
                0x009E,  # TLS_DHE_RSA_WITH_AES_128_GCM_SHA256
            ],
        )
    ]
)

print("\nClientHello message structure:")
print("  version: TLS 1.2")
print("  ciphers: List of encryption algorithms client supports")
print("  extensions: Additional features (SNI, ALPN, etc.)")
print()
print("Hex Dump of ClientHello:")
_ = hexdump(client_hello)

print()
print("Server responds with ServerHello, choosing one cipher from the list.")
print("Then both sides use that cipher to encrypt all subsequent data.")

# ============================================================================
# CIPHER SUITES EXPLANATION
# ============================================================================

print()
section_sep()
print("WHAT ARE CIPHER SUITES?")
section_sep()

print("\nCipher suite = Recipe for encryption")
print()
print("Example: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256")
print()
print("Breaking it down:")
print("  TLS           = Protocol")
print("  ECDHE         = Key exchange method (how to agree on secret key)")
print("  RSA           = Authentication method (verify server identity)")
print("  AES_128_GCM   = Encryption algorithm (scramble the data)")
print("  SHA256        = Hash function (verify data integrity)")
print()
print("Client offers many cipher suites. Server picks one they both support.")
print("Modern ciphers (like this one) provide:")
print("  - Forward secrecy (past communications stay secret)")
print("  - Strong encryption (AES-128 is industry standard)")
print("  - Authentication (RSA verifies server identity)")

print()
section_sep()
print("WHY THIS MATTERS")
section_sep()

print("\nWithout TLS:")
print("  - Passwords transmitted in plaintext")
print("  - Session cookies stolen")
print("  - Credit card numbers visible")
print("  - Personal data exposed")
print()
print("With TLS (HTTPS):")
print("  - All HTTP data encrypted")
print("  - Man-in-the-middle attacks prevented")
print("  - Data integrity verified")
print("  - Server identity authenticated")
print()
print("Always use HTTPS for:")
print("  - Login pages")
print("  - Payment forms")
print("  - Personal information")
print("  - Any sensitive communication")
print()
print("Look for the padlock icon in your browser!")

# Add spacing before FAQ
print("\n\n\n\n")

# ============================================================================
# PRINTED FAQ (for program output / website)
# ============================================================================

section_sep()
print("FREQUENTLY ASKED QUESTIONS")
section_sep()

print("\nQ: What does the 'S' in HTTPS stand for?")
example_sep()
print("""
S = Secure

HTTPS = HyperText Transfer Protocol Secure

It's the same HTTP protocol you already know, but wrapped in TLS encryption.

  HTTP:  Client -> [readable data] -> Server
  HTTPS: Client -> [encrypted data] -> Server

The encryption is transparent to your application. Your browser handles
all the TLS complexity automatically.
""")

print("\nQ: What is TLS? What is SSL? Are they different?")
example_sep()
print("""
SSL = Secure Sockets Layer (old, deprecated)
TLS = Transport Layer Security (modern, current)

History:
  1995: SSL 2.0 (had security flaws)
  1996: SSL 3.0 (better, but still flawed)
  1999: TLS 1.0 (renamed and improved SSL 3.0)
  2006: TLS 1.1
  2008: TLS 1.2 (widely used today)
  2018: TLS 1.3 (current standard)

Today:
  - SSL is completely deprecated (insecure)
  - TLS is what everyone uses
  - People still say "SSL" out of habit, but they mean TLS

When you see:
  - "SSL certificate" -> Really means TLS certificate
  - "SSL/TLS" -> Just means TLS (SSL mentioned for legacy reasons)
  - HTTPS -> Uses TLS (not SSL)

Use TLS 1.2 or TLS 1.3. Never use SSL.
""")

print("\nQ: What other protocols use TLS/SSL for encryption?")
example_sep()
print("""
TLS can encrypt ANY TCP-based protocol. Common examples:

1. HTTPS (HTTP over TLS)
   - Port 443
   - Web browsing, APIs, web applications
   - Most common use of TLS

2. FTPS (FTP over TLS)
   - Ports 989/990
   - Secure file transfer
   - Note: Different from SFTP (which uses SSH, not TLS)

3. SMTPS (SMTP over TLS)
   - Port 465/587
   - Sending email securely
   - Prevents email interception

4. IMAPS (IMAP over TLS)
   - Port 993
   - Receiving email securely
   - Protects email credentials and content

5. POP3S (POP3 over TLS)
   - Port 995
   - Another email protocol (older than IMAP)
   - Also benefits from TLS encryption

The pattern: Take any plaintext protocol, wrap it in TLS, and you get
the secure version. Usually indicated by adding an 'S' to the name.

TLS works at the transport layer, so it can protect any application
protocol that runs over TCP.
""")

print("\nQ: Does every request need a new TLS handshake and encryption key?")
example_sep()
print("""
NO! TLS handshake happens ONCE per TCP connection, just like TCP handshake.

Here's how a typical HTTPS session works:

1. TCP Handshake (once):
   Client -> Server: SYN, SYN-ACK, ACK
   [TCP connection established]

2. TLS Handshake (once):
   Client -> Server: ClientHello
   Server -> Client: ServerHello, Certificate, etc.
   [Encryption keys established]

3. Send many encrypted HTTP requests (reusing same session):
   Client -> Server: Encrypted HTTP Request 1
   Server -> Client: Encrypted HTTP Response 1
   Client -> Server: Encrypted HTTP Request 2
   Server -> Client: Encrypted HTTP Response 2
   [All use the SAME encryption key from step 2]

4. Connection closes:
   TCP connection closes (FIN-ACK)
   TLS session ends automatically

How does the server know it's the same client?

The TLS session is tied to the TCP connection:
  - Same TCP connection = same TLS session
  - Same source port + destination port = same connection
  - As long as TCP connection is open, TLS session is valid

The encryption key is stored in memory for this connection:
  - Browser stores: "Connection to example.com:443 uses key XYZ"
  - Server stores: "Connection from 192.168.1.100:54321 uses key XYZ"
  - They use the same key for all data on this connection

When does the session end?

The TLS session ends when the TCP connection closes:
  - Idle timeout (60-120 seconds of no activity)
  - Explicit close (browser navigates away)
  - Connection error (network failure)
  - New TCP connection = new TLS handshake required

Session Resumption (advanced):
  - Some browsers can resume TLS sessions across new TCP connections
  - Uses session IDs or session tickets
  - Avoids full handshake, faster reconnection
  - But still requires a partial handshake

Key insight:
  TCP connection = physical phone line
  TLS session = secret code you agreed on
  - Open the phone line once (TCP handshake)
  - Agree on secret code once (TLS handshake)
  - Talk many times using that code (many HTTP requests)
  - Hang up when done (TCP close, TLS ends)

Typical web page load:
  1. TCP handshake (once)
  2. TLS handshake (once)
  3. GET /index.html (encrypted with TLS)
  4. GET /style.css (encrypted with SAME key)
  5. GET /script.js (encrypted with SAME key)
  6. GET /logo.png (encrypted with SAME key)
  7. Connection stays open for more requests...

Only ONE TCP handshake and ONE TLS handshake for dozens of requests!
This is much more efficient than re-establishing security for every request.
""")

section_sep()
