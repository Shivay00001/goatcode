from typing import Dict, List, Any
from pathlib import Path

class ContextManager:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def get_context(self) -> Dict[str, Any]:
        return {
            "project_path": str(self.project_path),
            "files": [str(f) for f in self.project_path.glob("**/*") if f.is_file()][:100]
        }
