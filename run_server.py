#!/usr/bin/env python3
"""Entry point for running the TransitMCP server."""

import asyncio
from src.transitmcp.server import main

if __name__ == "__main__":
    asyncio.run(main())
