from typing import Dict, List, Any, Optional

class MemorySystem:
    def __init__(self):
        self.memories = []
    
    async def store(self, pattern: Dict[str, Any]):
        self.memories.append(pattern)
    
    async def lookup(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        # Simple text match for now
        return [m for m in self.memories if query.lower() in str(m).lower()][:limit]
