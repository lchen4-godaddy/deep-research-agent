from typing import Dict, Any, Optional, List, Tuple
from agents import SQLiteSession

class AgentMemory:
    """
    Centralized memory management for agent state and tool outputs.
    Uses SQLiteSession for conversation history and singleton pattern for global access.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            # Session for conversation history - using SQLiteSession directly since tool outputs are now stored in AgentMemory
            self.session = SQLiteSession("deep_research_session")
            
            # Tool outputs stored in local memory
            self._tool_outputs: Dict[str, Any] = {}
            
            # Research dump: Dictionary with [research question, list of (url, summary) tuples]
            self._research_dump: Dict[str, List[Tuple[str, str]]] = {}
            
            # Agent state flags
            self.has_enough_context: bool = False
            self.plan_finalized: bool = False
            self.research_finished: bool = False
            self.report_generated: bool = False
            
            self._initialized = True
    
    # Session conversation history management methods

    async def add_items(self, items: List[Dict[str, str]]) -> None:
        """Add items to the session conversation history."""
        await self.session.add_items(items)
    
    async def get_items(self) -> List[Any]:
        """Get all items from the session conversation history."""
        return await self.session.get_items()

    # Tool outputs management methods

    async def store_tool_output(self, tool_name: str, data: Any) -> None:
        """Store structured tool output data. Overwrites any previous output from the same tool."""
        self._tool_outputs[tool_name] = data
    
    async def get_tool_output(self, tool_name: str) -> Optional[Any]:
        """Retrieve structured tool output data."""
        return self._tool_outputs.get(tool_name)
    
    async def get_all_tool_outputs(self) -> Dict[str, Any]:
        """Get all stored tool outputs."""
        return self._tool_outputs.copy()
    
    async def clear_tool_outputs(self) -> None:
        """Clear all stored tool outputs."""
        self._tool_outputs.clear()

    # Research dump management methods

    async def add_to_research_dump(self, research_question: str, research_data: List[Tuple[str, str]]) -> None:
        """Add an entry to the research dump."""
        if research_question not in self._research_dump:
            self._research_dump[research_question] = []
        self._research_dump[research_question].extend(research_data)

    async def get_from_research_dump_by_question(self, research_question: str) -> List[Tuple[str, str]]:
        """Get all entries from the research dump for a given research question."""
        return self._research_dump.get(research_question, [])
    
    async def clear_research_dump(self) -> None:
        """Clear the research dump."""
        self._research_dump.clear()
    

    # State management methods

    def get_state(self, state: str) -> bool:
        """Get any state dynamically."""
        if hasattr(self, state):
            return getattr(self, state)
        else:
            raise ValueError(f"Unknown state: {state}")
    
    def set_state(self, state: str, value: bool) -> None:
        """Set any state dynamically."""
        if hasattr(self, state):
            setattr(self, state, value)
        else:
            raise ValueError(f"Unknown state: {state}")
    

# Global instance for easy import
AGENT_MEMORY = AgentMemory()