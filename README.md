# TCP/IP From Scratch

**A visual explanation of the TCP/IP model for web developers.**

Learn what actually happens when you make an HTTP request by seeing the actual bytes at each protocol layer.

## Examples

Two comprehensive examples with hex dumps, byte breakdowns, and FAQs:

1. **[01-foundations.py output](https://raw.githubusercontent.com/shipurjan/tcp-ip-from-scratch/refs/heads/master/examples/01-foundations.out.txt)** - All 4 TCP/IP layers explained

2. **[02-tls-https.py output](https://raw.githubusercontent.com/shipurjan/tcp-ip-from-scratch/refs/heads/master/examples/02-tls-https.out.txt)** - TLS/HTTPS encryption

Source code is in the `examples/` directory.

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

I built this with [Claude Code](https://claude.com/claude-code) to better understand the TCP/IP model. I wanted to see each layer visually and asked it questions to fill the gaps in my knowledge.

The FAQ sections came from those real questions - no question was too stupid.

## License

MIT License
