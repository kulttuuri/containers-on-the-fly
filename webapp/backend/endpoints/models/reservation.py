from pydantic import BaseModel
from typing import Dict, Any

class ReservationFilters(BaseModel):
    '''
    Filters for reservations.
    '''
    filters: Dict[str, Any]