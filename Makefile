.PHONY: server

server:
	fastmcp run server.py:mcp --transport http --host 0.0.0.0 --port 8787

