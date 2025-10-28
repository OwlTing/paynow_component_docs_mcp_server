# PayNow Component MCP Server

## Overview
The PayNow Component MCP Server provides documentation search capabilities. This server enables large language models (LLMs) to directly retrieve documentation, accelerating system integration.

<img src="./docs/Demo_paynow_component.gif" width="650">
<br><br>

## Components

### Tools

#### Query Tools
- `search_paynow_component_documentation`
   - Search PayNow Component documentation. 
   - Input:
     - `query` (string): Search keywords in English.
   - Returns: Query results as array of objects

## Install

For quick installation, use one of the one-click install buttons above. The remote MCP Server is hosted by PayNow and provides the easiest method for getting up and running. If your MCP host does not support remote MCP servers, you can easily set up the local version using Docker.


Docker Setup (For Local MCP Server Only):

```bash
docker build -f Dockerfile.local_docker -t mcp/paynow_component . --no-cache
```

<details>
<summary><b>Install in Cursor</b></summary>

#### Click the button to install:

[![Install in Cursor](https://img.shields.io/badge/Cursor-Install%20PayNow%20Component-blue?logo=cursor&logoColor=white)](https://owlting.github.io/paynow_component_docs_mcp_server/install-cursor-mcp.html)

#### Or install manually:

Go to `Cursor Settings` -> `Tools & Integrations` -> `New MCP Server`. 

```json
{
  "mcpServers": {
    "paynow_component": {
      "url": "https://paynow-component-docs-mcp.paynow.com.tw/mcp/"
    }
  }
}
```

### Docker
```json
{
  "mcpServers": {
    "paynow_component": {
      "command": "docker",
      "args": [
        "run", 
        "-i", 
        "--rm", 
        "mcp/paynow_component"
      ]
    }
  }
}
```
</details>

<details><summary><b>Install in VS Code</b></summary>

#### Click the button to install:
[![Install in VS Code](https://img.shields.io/badge/VS%20Code-Install%20PayNow%20Component-blue?logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect?url=vscode:mcp/install?%7B%22name%22%3A%22paynow_component%22%2C%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fpaynow-component-docs-mcp.paynow.com.tw%2Fmcp%2F%22%7D)

#### Or install manually:

You can also install the MCP server using the VS Code CLI:

```json
{
  "servers": {
    "paynow_component": {
      "type": "http",
      "url": "https://paynow-component-docs-mcp.paynow.com.tw/mcp/"
    }
  }
}
```

### Docker
```json
{
  "servers": {
    "paynow_component": {
      "command": "docker",
      "args": [
        "run", 
        "-i", 
        "--rm", 
        "mcp/paynow_component"
      ]
    }
  }
}
```
</details>


<details>
<summary><b>Install in Claude Desktop</b></summary>

Follow the MCP install [guide](https://modelcontextprotocol.io/quickstart/user), use following configuration:

```json
# Add the server to your claude_desktop_config.json
{
  "mcpServers": {
    "paynow_component": {
      "command": "docker",
      "args": [
        "run", 
        "-i", 
        "--rm", 
        "mcp/paynow_component"
      ]
    }
  }
}
```
</details>