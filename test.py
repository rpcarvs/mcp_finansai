# Pseudocode – exact client API may vary with your MCP client
import asyncio

from fastmcp import Client


async def main():
    client = Client("http://localhost:9001/mcp")
    async with client:
        result = await client.call_tool("get_financial_news", {"ticker": "AAPL", "company": "Apple", "model": "llama3"})
    print(result)


asyncio.run(main())
