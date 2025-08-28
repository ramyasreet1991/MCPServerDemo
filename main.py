#!/usr/bin/env python3
"""
MCP Server Entry Point
Centralizes access to Jira, Bitbucket, Confluence, and Outlook APIs
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server.server import MCPServer
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main entry point for the MCP server"""
    try:
        # Load configuration
        config = Config()
        
        # Initialize and start the MCP server
        server = MCPServer(config)
        await server.start()
        
        logger.info("MCP Server started successfully")
        
        # Keep the server running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down MCP Server...")
            await server.stop()
            
    except Exception as e:
        logger.error(f"Failed to start MCP Server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
