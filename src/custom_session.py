from agents import SQLiteSession
from typing import Dict, Any, Optional


class CustomSession(SQLiteSession):
    """Extended session that can store structured tool outputs and additional context or reference information."""
    
    def __init__(self, session_id: str, **kwargs):
        super().__init__(session_id, **kwargs)
        self._tool_output_data: Dict[str, Any] = {}
    
    async def store_tool_output(self, tool_name: str, data: Any) -> None:
        """Store structured tool output data. Overwrites any previous output from the same tool."""
        self._tool_output_data[tool_name] = data
    
    async def get_tool_output(self, tool_name: str) -> Optional[Any]:
        """Retrieve structured tool output data."""
        return self._tool_output_data.get(tool_name)
    
    async def get_all_tool_outputs(self) -> Dict[str, Any]:
        """Get all stored tool outputs."""
        return self._tool_output_data.copy()
    
    async def clear_tool_outputs(self) -> None:
        """Clear all stored tool outputs."""
        self._tool_output_data.clear() 