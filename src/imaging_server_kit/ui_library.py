from typing import Literal, List

# TODO: add missing UI elements

class UIElement:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description
        self.type = str
        self.widget_type = None


class DropDownUI(UIElement):
    def __init__(self, title, description, items: List, default: str):
        super().__init__(title, description)
        self.type = Literal[*items]  # From Python > 3.11
        self.default = default
        self.widget_type = "dropdown"


class FloatSpinBoxUI(UIElement):
    def __init__(self, title, description, min: float, max: float, step: float, default: float):
        super().__init__(title, description)
        self.min = min
        self.max = max
        self.step = step
        self.type = float
        self.default = default
        self.widget_type = "float"


class IntSpinBoxUI(UIElement):
    def __init__(self, title, description, min: int, max: int, step: int, default: int):
        super().__init__(title, description)
        self.min = min
        self.max = max
        self.step = step
        self.type = int
        self.default = default
        self.widget_type = "int"


class ImageUI(UIElement):
    def __init__(self, title, description, dimensionality: List[int]):
        super().__init__(title, description)
        self.widget_type = "image"
        self.dimensionality = dimensionality