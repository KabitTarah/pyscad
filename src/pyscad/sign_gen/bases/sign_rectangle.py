from abc import ABC, abstractmethod
from dataclasses import dataclass
from pythonscad import cube

from pyscad.sign_gen.bases.sign_shape import SignShape

class SignRectangle(SignShape):
    """
    Rectangular Sign
    """
    def build_base(self) -> object:
        self.base = cube([
            self.params.base_width_mm,
            self.params.base_height_mm,
            self.params.base_thickness_mm,
        ]).color(self.params.base_color)
        return self.base

    def build_border(self) -> object:
        border_1 = cube([
            self.params.base_width_mm - 2 * self.params.border_gap_mm,
            self.params.base_height_mm - 2 * self.params.border_gap_mm,
            self.params.border_height_mm,
        ]).translate([
            self.params.border_gap_mm,
            self.params.border_gap_mm,
            0,
        ])
        border_2 = cube([
            self.params.base_width_mm - 2 * self.params.border_gap_mm - 2 * self.params.border_thickness_mm,
            self.params.base_height_mm - 2 * self.params.border_gap_mm - 2 * self.params.border_thickness_mm,
            self.params.border_height_mm,
        ]).scale([1,1,1.1]).translate([
            self.params.border_gap_mm + self.params.border_thickness_mm,
            self.params.border_gap_mm + self.params.border_thickness_mm,
            -0.01
        ])
        self.border = border_1.difference(border_2).translate([
            0,
            0,
            self.params.base_thickness_mm,
        ]).color(self.params.border_color)

        return self.border
