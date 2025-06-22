import asyncio, json, os, sys, subprocess, textwrap
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.shared.session import StdioServerParameters

async def main():
    # --- exact Python inside the venv, plus -u for unbuffered IO ----
    python_exe = sys.executable            # e.g. C:\…\clickup-mcp-demo\.venv\Scripts\python.exe
    srv = StdioServerParameters(
        command=python_exe,
        args=["-u", "server/main.py"],     # <- -u fixes buffering
        log_stderr=True,                   # show server crashes in our console
    )

    async with stdio_client(srv) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()

            # --------------- call your ClickUp tool ----------------
            result = await s.call_tool(
                "create_task",
                {"name": "Demo via client", "description": "hello MCP"}
            )
            print("\nCreate-task response:\n", json.dumps(result, indent=2))

            # ----- tidy up so you don’t leave a stray task ----------
            task_id = result["task_id"]
            await s.call_tool("delete_task", {"task_id": task_id})
            print("\nDeleted task", task_id)

asyncio.run(main())
