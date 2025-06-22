from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio, json

async def main():
    # Tell the client *how* to start your server
    srv = StdioServerParameters(command="python", args=["server/main.py"])
    async with stdio_client(srv) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            # -- Call your tool -----------------------------
            result = await s.call_tool("create_task", {"name": "Demo via client"})
            print("Create result:", json.dumps(result, indent=2))

asyncio.run(main())
