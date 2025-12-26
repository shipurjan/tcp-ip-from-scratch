# TCP/IP From Scratch

**A visual explanation of the TCP/IP model for web developers.**

Learn what actually happens when you make an HTTP request by seeing the actual bytes at each protocol layer.

## Examples

Two comprehensive examples with hex dumps, byte breakdowns, and FAQs:

1. **[01-foundations.py](examples/01-foundations.py)** - All 4 TCP/IP layers explained
   - [Read the full output](examples/01-foundations.out.txt)

2. **[02-tls-https.py](examples/02-tls-https.py)** - TLS/HTTPS encryption
   - [Read the full output](examples/02-tls-https.out.txt)

## Running the Examples

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/yourusername/tcp-ip-from-scratch.git
cd tcp-ip-from-scratch
uv sync

# Run examples
uv run python examples/01-foundations.py
uv run python examples/02-tls-https.py
```

## About

I built this repository using [Claude Code](https://claude.com/claude-code) to better understand the TCP/IP model. I wanted to see each layer visually with actual hex dumps and byte breakdowns.

The FAQ sections came from real questions I asked while learning - no question was too basic. If you're confused about something, the answer is probably in the FAQ.

## License

MIT License
