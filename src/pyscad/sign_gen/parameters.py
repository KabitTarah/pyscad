from dataclasses import dataclass

@dataclass
class BaseParameters:
    base_thickness_mm: float = 5
    base_height_mm: float = 60
    base_width_mm: float = 150
    base_color: str = "brown"

    top_item: bool = True
    top_item_width_mm: float = 95
    top_item_height_mm: float = 35

    bottom_item: bool = True
    bottom_item_width_mm: float = 95
    bottom_item_height_mm: float = 35

    border_thickness_mm: float = 2
    border_height_mm: float = 2
    border_gap_mm: float = 2
    border_color: str = "black"
