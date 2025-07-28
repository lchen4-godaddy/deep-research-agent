from typing import Dict, Any, Optional, List
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
            
            # Agent state flags
            self.has_enough_context: bool = False
            self.plan_finalized: bool = False
            self.research_finished: bool = False
            self.report_generated: bool = False
            
            # Tool outputs stored directly in memory
            self.research_plan: Optional[str] = None
            self.plan_summary: Optional[str] = None
            self.research_dump: Optional[str] = None
            self.report_md: Optional[str] = None
            
            self._initialized = True
    
    async def store_tool_output(self, tool_name: str, data: Any) -> None:
        """Store structured tool output data. Overwrites any previous output from the same tool."""
        self._tool_outputs[tool_name] = data
        
        # Special handling for research plan and plan summary
        if tool_name == "plan_writer_tool":
            self.research_plan = data
        elif tool_name == "plan_summarizer_tool":
            self.plan_summary = data
        elif tool_name == "research_tool":
            self.research_dump = data
        elif tool_name == "report_writer_tool":
            self.report_md = data
    
    async def get_tool_output(self, tool_name: str) -> Optional[Any]:
        """Retrieve structured tool output data."""
        return self._tool_outputs.get(tool_name)
    
    async def get_all_tool_outputs(self) -> Dict[str, Any]:
        """Get all stored tool outputs."""
        return self._tool_outputs.copy()
    
    async def clear_tool_outputs(self) -> None:
        """Clear all stored tool outputs."""
        self._tool_outputs.clear()
        self.research_plan = None
        self.plan_summary = None
        self.research_dump = None
        self.report_md = None
    
    async def add_items(self, items: List[Dict[str, str]]) -> None:
        """Add items to the session conversation history."""
        await self.session.add_items(items)
    
    async def get_items(self) -> List[Any]:
        """Get all items from the session conversation history."""
        return await self.session.get_items()
    
    # Convenience methods for research plan and summary
    async def get_research_plan(self) -> Optional[str]:
        """Get the research plan directly from memory."""
        return self.research_plan
    
    async def get_plan_summary(self) -> Optional[str]:
        """Get the plan summary directly from memory."""
        return self.plan_summary
    
    async def get_research_dump(self) -> Optional[str]:
        """Get the research dump directly from memory."""
        return self.research_dump
    
    async def get_report_md(self) -> Optional[str]:
        """Get the report markdown directly from memory."""
        return self.report_md
    
    async def set_research_plan(self, plan: str) -> None:
        """Set the research plan directly in memory."""
        self.research_plan = plan
        await self.store_tool_output("plan_writer_tool", plan)
    
    async def set_plan_summary(self, summary: str) -> None:
        """Set the plan summary directly in memory."""
        self.plan_summary = summary
        await self.store_tool_output("plan_summarizer_tool", summary)
    
    async def set_research_dump(self, dump: str) -> None:
        """Set the research dump directly in memory."""
        self.research_dump = dump
        await self.store_tool_output("research_tool", dump)
    
    async def set_report_md(self, md: str) -> None:
        """Set the report markdown directly in memory."""
        self.report_md = md
        await self.store_tool_output("report_writer_tool", md)

    # State management methods
    def set_has_enough_context(self, value: bool) -> None:
        """Set the has_enough_context flag."""
        self.has_enough_context = value
    
    def set_plan_finalized(self, value: bool) -> None:
        """Set the plan_finalized flag."""
        self.plan_finalized = value
    
    def set_research_finished(self, value: bool) -> None:
        """Set the research_finished flag."""
        self.research_finished = value
    
    def set_report_generated(self, value: bool) -> None:
        """Set the report_generated flag."""
        self.report_generated = value
    
    def get_has_enough_context(self) -> bool:
        """Get the has_enough_context flag."""
        return self.has_enough_context
    
    def get_plan_finalized(self) -> bool:
        """Get the plan_finalized flag."""
        return self.plan_finalized
    
    def get_research_finished(self) -> bool:
        """Get the research_finished flag."""
        return self.research_finished
    
    def get_report_generated(self) -> bool:
        """Get the report_generated flag."""
        return self.report_generated

# Global instance for easy import
AGENT_MEMORY = AgentMemory()