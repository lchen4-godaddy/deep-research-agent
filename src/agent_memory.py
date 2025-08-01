from typing import Dict, Any, List, Tuple
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
            # Session for conversation history
            self.session = SQLiteSession("deep_research_session")
            
            # Research plan: String containing the research plan
            self._research_plan: str = ""
            
            # Research dump: Dictionary with [research question, list of ((title, url), summary) tuples]
            self._research_dump: Dict[str, List[Tuple[Tuple[str, str], str]]] = {}
            
            # Report: String containing the report
            self._research_report: str = ""
            
            # Agent state flags
            self.has_enough_context: bool = False
            self.plan_generated: bool = False
            self.plan_finalized: bool = False
            self.report_generated: bool = False
            
            self._initialized = True
    
    # Session conversation history management methods

    async def add_items(self, items: List[Dict[str, str]]) -> None:
        """Add items to the session conversation history."""
        await self.session.add_items(items)
    
    async def get_items(self) -> List[Any]:
        """Get all items from the session conversation history."""
        return await self.session.get_items()

    async def clear_session(self) -> None:
        """Clear the session."""
        await self.session.clear()

    # Research plan management methods

    async def store_research_plan(self, research_plan: str) -> None:
        """Store the research plan."""
        self._research_plan = research_plan

    async def get_research_plan(self) -> str:
        """Get the stored research plan."""
        return self._research_plan

    async def clear_research_plan(self) -> None:
        """Clear the research plan."""
        self._research_plan = ""

    # Research dump management methods

    async def add_to_research_dump(self, research_question: str, research_data: List[Tuple[Tuple[str, str], str]]) -> None:
        """Add an entry to the research dump."""
        if research_question not in self._research_dump:
            self._research_dump[research_question] = []
        self._research_dump[research_question].extend(research_data)

    async def get_from_research_dump_by_question(self, research_question: str) -> List[Tuple[Tuple[str, str], str]]:
        """Get all entries from the research dump for a given research question."""
        return self._research_dump.get(research_question, [])

    async def get_research_dump(self) -> Dict[str, List[Tuple[Tuple[str, str], str]]]:
        """Get the research dump."""
        return self._research_dump
    
    async def clear_research_dump(self) -> None:
        """Clear the research dump."""
        self._research_dump.clear()

    # Report management methods

    async def store_report(self, report: str) -> None:
        """Store the report."""
        self._research_report = report

    async def get_report(self) -> str:
        """Get the report."""
        return self._research_report

    async def clear_report(self) -> None:
        """Clear the report."""
        self._research_report = ""

    # State management methods

    def get_state(self, state: str) -> bool:
        """Get any state dynamically."""
        if hasattr(self, state):
            return getattr(self, state)
        else:
            # Log the missing state but return False instead of raising an error
            print(f"Warning: Unknown state '{state}' requested. Returning False.")
            return False
    
    def set_state(self, state: str, value: bool) -> None:
        """Set any state dynamically."""
        if hasattr(self, state):
            setattr(self, state, value)
        else:
            # Log the missing state but don't raise an error
            print(f"Warning: Unknown state '{state}' cannot be set. State may not be defined in AgentMemory.")
    

# Global instance for easy import
AGENT_MEMORY = AgentMemory()