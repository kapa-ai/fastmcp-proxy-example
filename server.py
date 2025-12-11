"""
Federated MCP Server Example

Shows how to integrate Kapa AI's retrieval tool into your existing MCP server.
"""

import os
import sys
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

KAPA_MCP_SERVER_URL = os.getenv("KAPA_MCP_SERVER_URL")
KAPA_API_KEY = os.getenv("KAPA_API_KEY")

if not KAPA_MCP_SERVER_URL or not KAPA_API_KEY:
    sys.exit("❌ KAPA_MCP_SERVER_URL and KAPA_API_KEY must be set in .env")


async def create_server() -> FastMCP:
    """Factory function that creates the server with Kapa integration."""
    
    mcp = FastMCP(name="My Product MCP Server")

    # Your native tool
    @mcp.tool
    def get_status() -> dict:
        """Get the current system status."""
        return {"status": "healthy", "version": "1.0.0"}

    # Import Kapa's retrieval tool
    print(f"🔗 Connecting to Kapa: {KAPA_MCP_SERVER_URL}", file=sys.stderr, flush=True)
    
    kapa_proxy = FastMCP.as_proxy(
        {
            "mcpServers": {
                "kapa": {
                    "url": KAPA_MCP_SERVER_URL,
                    "transport": "http",
                    "headers": {"Authorization": f"Bearer {KAPA_API_KEY}"}
                }
            }
        },
        name="Kapa"
    )
    
    await mcp.import_server(kapa_proxy)
    print("✅ Kapa tools imported", file=sys.stderr, flush=True)

    return mcp


if __name__ == "__main__":
    import asyncio
    mcp = asyncio.run(create_server())
    mcp.run()
