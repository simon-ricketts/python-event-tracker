from dataclasses import dataclass
from typing import Dict

from src.dimension import Dimension


@dataclass
class DataStruct:
    website_url: str
    session_id: str
    resize_from: Dimension
    resize_to: Dimension
    copy_and_paste: Dict[str, bool]
    form_completion_time: int
