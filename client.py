from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
import asyncio

server = "http://0.0.0.0:8000/mcp"

async def main():
    config = {"configurable": {"thread_id": 1234}}
    async with streamablehttp_client(server) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Check available tools
            tools = await session.list_tools()
            # print("Available tools:", [tool.name for tool in tools])
            for tag in tools:
                if (tag[-1]):
                    for tool in tag[-1]:
                        print(f"Tool: {tool.name}, Description: {tool.description}")

if __name__ == "__main__":
    asyncio.run(main())