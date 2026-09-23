# Works both when installed as top-level packages (pip install .) and when
# imported as the `goatcode` package (e.g. `goatcode.core.tool_registry`).
try:
    from ..tools.registry import ToolRegistry
except ImportError:
    from tools.registry import ToolRegistry

__all__ = ['ToolRegistry']
