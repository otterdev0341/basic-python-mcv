from dataclasses import dataclass, field
from mcp.server.fastmcp import FastMCP  # type: ignore
from di_container import DIContainer
from typing import Any, Callable, Protocol
import re


class MCPProtocol(Protocol):
    def resource(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...
    def tool(self) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...
    def start(self) -> None: ...


@dataclass
class MCPServer:
    name: str
    _container: DIContainer
    _mcp: Any = field(init=False)  # FastMCP is dynamically typed

    def __post_init__(self):
        self._mcp = FastMCP(self.name)

    def resource(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        method, route_path = self._translate_path_and_method(path)
        return self._mcp.resource(route_path, method=method)

    def tool(self) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self._mcp.tool()

    def start(self) -> None:
        self._mcp.start()

    def _translate_path_and_method(self, uri: str) -> tuple[str, str]:
        """
        Converts custom URI schemes like 'contact://create' to
        ('POST', '/contact/create') or 'GET', 'DELETE', etc.
        """
        # Extract scheme and path
        match = re.match(r"^(\w+)://(.+)$", uri)
        if not match:
            raise ValueError(f"Invalid resource URI: {uri}")

        scheme, raw_path = match.groups()
        parts = raw_path.strip("/").split("/")

        # Determine method
        if parts[-1] == "create":
            method = "POST"
        elif parts[-1] == "delete":
            method = "DELETE"
        elif parts[-1] == "update":  # Detect update operation
            method = "PUT"  # Use PUT for update
        elif any("{" in part for part in parts):
            method = "GET"
        else:
            method = "GET"

        # Translate to FastAPI-compatible path
        route_path = f"/{scheme}/{'/'.join(parts)}"
        return method, route_path
