from fastmcp import FastMCP, Client
import asyncio
from pydantic import BaseModel
import logging
from fastapi import FastAPI
import uvicorn
from starlette.routing import Mount

mcp = FastMCP(
    name="example_mcp",
)
# app = FastAPI()
# @app.get("/ping")
# async def ping():
#     return {"message": "pong"}
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Starting MCP server...")

@mcp.tool("example_tool")
def example_tool(input_text: str) -> str:
    """
    This is an example tool that echoes the input text.
    """
    logging.info("Received input: %s", input_text)
    return f"Received input: {input_text}"

@mcp.tool("addition_tool")
def addition_tool(a: int, b: int) -> int:
    """
    This tool adds two integers and returns the result.
    """
    logging.info("Adding %d and %d", a, b)
    return a + b


class CustomBody(BaseModel):
    """
    Custom body model for the body_check_tool.
    """
    name: str
    age: int

@mcp.tool("body_check_tool")
def body_check_tool(body: CustomBody) -> str:
    """
    This tool checks the body of the request and returns a message.
    """
    logging.info("Received body: %s", body)
    return f"Received body: {body}"


USER_PROFILES = {
    101: {"name": "Alice", "status": "active"},
    102: {"name": "Bob", "status": "inactive"},
}

@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: int) -> dict:
    """Retrieves a user's profile by their ID."""
    # The {user_id} from the URI is automatically passed as an argument
    logging.info("Retrieving profile for user_id: %d", user_id)
    return USER_PROFILES.get(user_id, {"error": "User not found"})

@mcp.resource("greet://{name}")
def greet(name: str) -> str:
    """Greets the user by their name."""
    logging.info("Greeting user: %s", name)
    return f"Hello, {name}!"


# app.router.routes.append(
#     Mount("/", app=mcp.sse_app())
# )

if __name__ == "__main__":
    # mcp.settings.port = 8000
    # uvicorn.run(
    #     app,
    #     host=mcp.settings.host,
    #     port=mcp.settings.port,   
    # )

    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = 8000
    mcp.run(transport="http")