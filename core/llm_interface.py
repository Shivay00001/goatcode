# Works both when installed as top-level packages (pip install .) and when
# imported as the `goatcode` package (e.g. `goatcode.core.llm_interface`).
try:
    from ..llm.interface import create_llm_interface, LLMResponse, BaseLLMInterface as LLMInterface
except ImportError:
    from llm.interface import create_llm_interface, LLMResponse, BaseLLMInterface as LLMInterface

__all__ = ['create_llm_interface', 'LLMResponse', 'LLMInterface']
