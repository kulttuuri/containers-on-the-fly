from pydantic import BaseModel
from typing import Dict, Any

class ContainerEdit(BaseModel):
    '''
    For editing a container.
    '''
    containerId: int
    data: Dict[str, Any]