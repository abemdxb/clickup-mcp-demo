import asyncio, json, sys
from mcp import ClientSession, StdioServerParameters          # <-- fixed
from mcp.client.stdio import stdio_client

async def main():
    srv = StdioServerParameters(
        command=sys.executable,           # the venv’s python
        args=["-u", "server/main.py"],    # -u = unbuffered I/O
        log_stderr=True,                  # show server crashes
    )

    async with stdio_client(srv) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()

            # create a task
            res = await s.call_tool(
                "create_task",
                {"name": "Demo via client", "description": "hello MCP"}
            )
            print("Created:", json.dumps(res, indent=2))

            # delete it again so ClickUp stays tidy
            await s.call_tool("delete_task", {"task_id": res["task_id"]})
            print("Deleted", res["task_id"])

asyncio.run(main())
