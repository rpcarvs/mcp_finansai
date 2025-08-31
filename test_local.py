# import asyncio

# from fastmcp import Client

# client = Client("social_mcp/app.py")


# async def main():
#     async with client:
#         result = await client.call_tool(
#             "get_financial_news", {"ticker": "AAPL", "company": "Apple", "model": "llama3.1:8b "}
#         )
#         print(result)


# asyncio.run(main())

# test_local.py
import asyncio

from fastmcp import Client


async def main():
    async with Client("http://localhost:9002/mcp") as client:
        result = await client.call_tool(
            "get_social_sentiment",
            {"ticker": "AAPL", "company": "Apple", "model": "llama3.1:8b"},
        )
        print(result)


asyncio.run(main())
