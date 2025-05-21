import asyncio
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from pydantic import BaseModel, Field

from mcp.shared.exceptions import McpError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    ErrorData,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)

PAYNOW_COMPONENT_DOCS_MCP_SERVER_API = (
    "https://mcp.owlting.com/paynow-component-docs/get-paynow-component-documentation"
)


class SearchArgs(BaseModel):
    """Parameters for searching PayNow Component documentation."""
    query: str = Field(..., description="Search keywords in English. Any non-English input will be auto-translated to English before populating this field.")

def search_paynow_component_documentation(query: str) -> str:
    """Call external PayNow Component API and return raw text or raise McpError."""
    try:
        session = requests.Session()
        session.mount("http://", HTTPAdapter(max_retries=3))
        resp = session.get(
            PAYNOW_COMPONENT_DOCS_MCP_SERVER_API, params={
                "query": query,
                "lang": "en",
                }, timeout=30
        )
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Failed to search documentation: {e!r}",
            )
        )


async def serve() -> None:
    """Run the search-paynow-component-documentation MCP server."""
    server = Server("search-paynow-component-documentation")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="search_paynow_component_documentation",
                description="Search PayNow Component documentation. Any non-English input will be auto-translated to English before populating the query.",
                inputSchema=SearchArgs.model_json_schema(),
            )
        ]

    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        return [
            Prompt(
                name="search_paynow_component_documentation",
                description="Search PayNow Component documentation and return matching sections",
                arguments=[
                    PromptArgument(
                        name="query",
                        description="Search query in English. Any non-English input will be auto-translated to English before filling this argument.",
                        required=True,
                    )
                ],
            )
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[TextContent]:
        try:
            args = SearchArgs(**(arguments or {}))
        except ValueError as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))

        result = search_paynow_component_documentation(args.query)
        return [TextContent(type="text", text=result)]

    @server.get_prompt()
    async def get_prompt(
        name: str, arguments: dict[str, Any] | None
    ) -> GetPromptResult:
        if not arguments or "query" not in arguments:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="Query is required"))
        try:
            result = search_paynow_component_documentation(arguments["query"])
        except McpError as e:
            return GetPromptResult(
                description="Search failed",
                messages=[PromptMessage(role="user", content=TextContent(type="text", text=str(e)))],
            )
        return GetPromptResult(
            description="Search results",
            messages=[PromptMessage(role="user", content=TextContent(type="text", text=result))],
        )

    options = server.create_initialization_options()
    async with stdio_server() as (r, w):
        await server.run(r, w, options, raise_exceptions=True)