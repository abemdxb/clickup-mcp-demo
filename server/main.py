# server/main.py  – ClickUp “mini MCP” (June 2025 style)

import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP      # ← NEW import

load_dotenv()

TOKEN   = os.getenv("CLICKUP_TOKEN")        # pulled from .env
LIST_ID = os.getenv("CLICKUP_LIST_ID")      # any list in your workspace
BASE    = "https://api.clickup.com/api/v2"
HEADERS = {"Authorization": TOKEN}

mcp = FastMCP("ClickUp Demo")               # ← NEW entry-point

def _call(method: str, url: str, payload: dict | None = None) -> dict:
    """Tiny helper around httpx so we don’t repeat headers/timeouts."""
    with httpx.Client(headers=HEADERS, timeout=10.0) as client:
        r = client.request(method.upper(), url, json=payload)
        r.raise_for_status()
        return r.json() if r.text else {}

# --------------------------  TOOLS  --------------------------

@mcp.tool(description="Create a new task in the configured ClickUp list")
def create_task(name: str, description: str | None = None) -> dict:
    data = _call("post", f"{BASE}/list/{LIST_ID}/task",
                 {"name": name, **({"description": description} if description else {})})
    return {"task_id": data["id"], "url": data["url"]}

@mcp.tool(description="Update a ClickUp task’s name and/or status")
def update_task(task_id: str,
                name: str | None = None,
                status: str | None = None) -> dict:
    if not (name or status):
        raise ValueError("Provide at least one of name or status")
    _call("put", f"{BASE}/task/{task_id}",
          {k: v for k, v in (("name", name), ("status", status)) if v})
    return {"ok": True}

@mcp.tool(description="Delete a ClickUp task forever")
def delete_task(task_id: str) -> dict:
    _call("delete", f"{BASE}/task/{task_id}")
    return {"ok": True}

# --------------------------  MAIN  --------------------------

if __name__ == "__main__":
    print("🚀 FastMCP ClickUp server ready (stdio mode)…")
    mcp.run()                                # FastMCP handles the event loop
