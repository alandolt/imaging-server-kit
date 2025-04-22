from typing import List
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class UIElement:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description
        self.type = str
        self.widget_type = None


class DropDownUI(UIElement):
    def __init__(self, title, description, items: List, default: str):
        super().__init__(title, description)
        # self.type = Literal[*items]  # From Python > 3.11
        self.type = Literal.__getitem__(tuple(items))
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


class BoolUI(UIElement):
    def __init__(self, title, description, default: bool):
        super().__init__(title, description)
        self.type = bool
        self.default = default
        self.widget_type = "bool"


class StringUI(UIElement):
    def __init__(self, title, description, default: str):
        super().__init__(title, description)
        self.type = str
        self.default = default
        self.widget_type = "str"


class ImageUI(UIElement):
    def __init__(self, title, description, dimensionality: List[int]):
        super().__init__(title, description)
        self.widget_type = "image"
        self.dimensionality = dimensionality


class MaskUI(UIElement):
    def __init__(self, title, description, dimensionality: List[int]):
        super().__init__(title, description)
        self.widget_type = "mask"
        self.dimensionality = dimensionality


class PointsUI(UIElement):
    def __init__(self, title, description, dimensionality: List[int]):
        super().__init__(title, description)
        self.widget_type = "points"
        self.dimensionality = dimensionality


class VectorsUI(UIElement):
    def __init__(self, title, description, dimensionality: List[int]):
        super().__init__(title, description)
        self.widget_type = "vectors"
        self.dimensionality = dimensionality


class ShapesUI(UIElement):
    def __init__(self, title, description):
        super().__init__(title, description)
        self.widget_type = "shapes"


class TracksUI(UIElement):
    def __init__(self, title, description):
        super().__init__(title, description)
        self.widget_type = "tracks"
