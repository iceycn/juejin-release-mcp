# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

掘金 MCP 服务器 (juejin-release-mcp) is a Model Context Protocol (MCP) server that enables AI assistants to manage Juejin (掘金) articles. It allows AI clients like Claude, Cursor, and Trae to publish articles, manage drafts, and interact with the Juejin platform through natural language.

## Architecture

The project follows a layered architecture:

```
src/user_juejin/
├── server.py              # MCP server entry point, tool definitions, and handlers
├── config.py              # Configuration management (JuejinConfig from env vars)
├── mcp_instructions.py    # MCP instructions sent to clients during initialization
├── clients/
│   └── juejin_client.py   # HTTP client for Juejin API interactions
├── services/
│   └── article_service.py # Business logic layer (publish, draft management)
└── models/
    ├── request.py         # Pydantic/dataclass models for API requests
    └── response.py        # Response models and parsing
```

Key design patterns:
- **Service Layer**: `ArticleService` encapsulates business logic like `publish_article()` which chains "create draft + publish" operations
- **Client Layer**: `JuejinClient` handles raw HTTP calls to Juejin's REST API (`api.juejin.cn`)
- **MCP Protocol**: Uses the official `mcp` Python SDK with stdio transport for communication

## Common Commands

### Development Setup
```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run the server locally (requires JUEJIN_COOKIE env var)
export JUEJIN_COOKIE="sessionid=xxx"
python -m src.user_juejin.server
```

### Testing
```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_models.py

# Run a specific test
pytest tests/test_models.py::test_create_draft_request
```

### Code Quality
```bash
# Linting (ruff)
ruff check src/
ruff check --fix src/

# Type checking (mypy)
mypy src/
```

### Building and Publishing
```bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `JUEJIN_COOKIE` | Yes | Juejin session cookie (format: `sessionid=xxx`) |
| `JUEJIN_AID` | No | App ID (default: 2608) |
| `JUEJIN_UUID` | No | User UUID |
| `JUEJIN_TIMEOUT` | No | Request timeout in seconds (default: 30) |
| `JUEJIN_MAX_RETRIES` | No | Max retries (default: 3) |

## Key Implementation Details

### MCP Tool Handlers
Tools are defined in `server.py` with two main handlers:
- `@server.list_tools()` - Returns tool schemas
- `@server.call_tool()` - Dispatches to appropriate service methods

### Article Publishing Flow
The `publish_article` tool in `ArticleService` performs:
1. Creates draft via `/content_api/v1/article_draft/create`
2. Publishes via `/content_api/v1/article/publish`
3. Returns article ID and link

### Request/Response Models
Located in `models/` directory using dataclasses with `to_api_dict()` methods for converting to Juejin's expected JSON format. Field names use snake_case internally but convert to camelCase for the API.

## PyPI Configuration

PyPI token is configured in `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-xxx
```

## Project Metadata

- **Package name**: `juejin-release-mcp`
- **Entry point**: `juejin-release-mcp` command (defined in `pyproject.toml`)
- **Python requirement**: >= 3.10
- **Build system**: hatchling
