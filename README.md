# Federated MCP Server Example

Integrate [Kapa AI's retrieval tool](https://docs.kapa.ai/integrations/mcp/overview) into your existing MCP server.

## Why?

Instead of giving users two separate MCP servers, proxy Kapa's tool into yours:

```
┌────────────────────────────────────┐
│       Your MCP Server              │
│                                    │
│  • get_status (native)             │
│  • search_*_knowledge_sources ─────┼──► Kapa MCP
│                                    │
└────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Configure
cp env.example .env
# Edit .env with your Kapa credentials

# 2. Start
docker compose up

# 3. Test with MCP Inspector
# Open http://localhost:6274
# Connect to http://host.docker.internal:8787/mcp
```

## How It Works

```python
from fastmcp import FastMCP

mcp = FastMCP(name="My Product MCP Server")

@mcp.tool
def get_status() -> dict:
    """Your native tool."""
    return {"status": "healthy"}

async def setup():
    # Create proxy to Kapa's MCP server
    kapa_proxy = FastMCP.as_proxy({
        "mcpServers": {
            "kapa": {
                "url": os.getenv("KAPA_MCP_SERVER_URL"),
                "transport": "http",
                "headers": {"Authorization": f"Bearer {os.getenv('KAPA_API_KEY')}"}
            }
        }
    })
    
    # Import copies tools at startup (fast, no runtime HTTP overhead)
    await mcp.import_server(kapa_proxy)

asyncio.run(setup())
mcp.run()
```

## Project Structure

```
├── server.py           # The MCP server
├── docker-compose.yml  # Dev environment with Inspector
├── Dockerfile
├── requirements.txt
└── env.example
```

## Configuration

Get credentials from [Kapa Dashboard](https://app.kapa.ai):

| Variable | Description |
|----------|-------------|
| `KAPA_MCP_SERVER_URL` | `https://your-project.mcp.kapa.ai` |
| `KAPA_API_KEY` | Your API key |

## Running Locally

```bash
pip install -r requirements.txt
python server.py

# Or with HTTP transport:
fastmcp run server.py --transport http --port 8787
```

## Resources

- [Kapa MCP Docs](https://docs.kapa.ai/integrations/mcp/overview)
- [FastMCP Proxy Servers](https://gofastmcp.com/servers/proxy)
- [FastMCP Server Composition](https://gofastmcp.com/servers/composition)
