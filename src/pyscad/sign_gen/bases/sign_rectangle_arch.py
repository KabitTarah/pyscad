from abc import ABC, abstractmethod
from dataclasses import dataclass
import math
from pythonscad import circle, cube

from pyscad.sign_gen.bases.sign_shape import SignShape

def chord_from_height_and_radius(height: float, radius: float) -> float:
    """
    Finds the chord length given the radius and height of the chord
    """
    theta = 2 * math.acos((radius - height) / radius)
    dist = 2 * radius * math.sin(theta / 2)
    return dist

def radius_from_chord(dist: float, height: float) -> float:
    """
    Finds the radius given chord length and height

    dist = base length of chord
    height = orthogonal distance from center of base to circle

    https://www.themathdoctors.org/how-to-find-any-part-of-a-segment-of-a-circle/
    """
    
    return (dist ** 2 + 4 * height ** 2) / (8 * height)

def build_chord_circle(dist: float, height: float, thickness: float, offset: float = 0) -> object:
    """
    Returns PythonSCAD object for the chord item normalized to origin
    """
    # First get circle:
    radius = radius_from_chord(dist, height)
    diam = radius * 2
    circ_obj = circle(r=radius).linear_extrude(height=thickness)

    cube_obj = cube(
        [diam+1, diam, thickness + 1], center=True
    ).translate([0, - height - offset, thickness/2])
    obj = circ_obj.difference(cube_obj).translate([0, height-radius, 0])
    return obj

def build_chord_border(
        dist: float,
        height: float,
        thickness: float,
        border_gap: float,
        border_thickness: float,
    ) -> object:
    """
    Returns PythonSCAD border object for the chord created with above
    """
    c1 = build_chord_circle(
        dist = dist - 2 * border_gap,
        height = height - border_gap,
        thickness = thickness,
        offset = border_gap,
    )
    c2 = build_chord_circle(
        dist = dist - 2 * border_gap - 2 * border_thickness,
        height = height - border_gap - border_thickness,
        thickness = thickness,
        offset = border_gap,
    )
    obj = c1.difference(c2)
    return obj

class SignRectangleArch(SignShape):
    """
    Rectangular Sign with circular top and bottom arch
    """
    def build_base(self) -> object:
        obj = cube([
            self.params.base_width_mm,
            self.params.base_height_mm,
            self.params.base_thickness_mm,
        ])
        top_obj = build_chord_circle(
            dist = self.params.top_item_width_mm,
            height = self.params.top_item_height_mm,
            thickness = self.params.base_thickness_mm,
        ).translate([
            self.params.base_width_mm / 2,
            self.params.base_height_mm,
            0
        ])
        if self.params.top_item:
            obj = obj.union(top_obj)

        bottom_obj = build_chord_circle(
            dist = self.params.bottom_item_width_mm,
            height = self.params.bottom_item_height_mm,
            thickness = self.params.base_thickness_mm,
        ).rotate([0,0,180]).translate([
            self.params.base_width_mm / 2,
            0,
            0
        ])
        if self.params.bottom_item:
            obj = obj.union(bottom_obj)

        self.base = obj.color(self.params.base_color)
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
        obj = border_1.difference(border_2)

        if self.params.top_item:
            radius = radius_from_chord(
                dist = self.params.top_item_width_mm,
                height = self.params.top_item_height_mm
            )
            offset_chord = chord_from_height_and_radius(
                height = self.params.top_item_height_mm + self.params.border_gap_mm,
                radius = radius
            )
            # Delete
            deletion = cube([
                offset_chord - 2 * self.params.border_gap_mm - 2 * self.params.border_thickness_mm,
                self.params.border_thickness_mm * 2,
                self.params.border_height_mm * 2,
            ]).translate([
                (self.params.base_width_mm - offset_chord) / 2 +
                  self.params.border_gap_mm + self.params.border_thickness_mm,
                self.params.base_height_mm - self.params.border_gap_mm - self.params.border_thickness_mm,
                -0.01
            ])
            obj = obj.difference(deletion)
            # Add
            top_border = build_chord_border(
                dist = self.params.top_item_width_mm,
                height = self.params.top_item_height_mm,
                thickness = self.params.border_height_mm,
                border_gap = self.params.border_gap_mm,
                border_thickness = self.params.border_thickness_mm,
            ).translate([
                self.params.base_width_mm / 2,
                self.params.base_height_mm,
                0
            ])
            obj = obj.union(top_border)

        if self.params.bottom_item:
            radius = radius_from_chord(
                dist = self.params.bottom_item_width_mm,
                height = self.params.bottom_item_height_mm
            )
            offset_chord = chord_from_height_and_radius(
                height = self.params.bottom_item_height_mm + self.params.border_gap_mm,
                radius = radius
            )
            # Delete
            deletion = cube([
                offset_chord - 2 * self.params.border_gap_mm - 2 * self.params.border_thickness_mm,
                self.params.border_thickness_mm * 2,
                self.params.border_height_mm * 2,
            ]).translate([
                (self.params.base_width_mm - offset_chord) / 2 +
                  self.params.border_gap_mm + self.params.border_thickness_mm,
                self.params.border_gap_mm,
                -0.01
            ])
            obj = obj.difference(deletion)
            # Add
            bottom_border = build_chord_border(
                dist = self.params.bottom_item_width_mm,
                height = self.params.bottom_item_height_mm,
                thickness = self.params.border_height_mm,
                border_gap = self.params.border_gap_mm,
                border_thickness = self.params.border_thickness_mm,
            ).rotate([0,0,180]).translate([
                self.params.base_width_mm / 2,
                0,
                0
            ])
            obj = obj.union(bottom_border)

        obj = obj.translate([
            0,
            0,
            self.params.base_thickness_mm,
        ])
        self.border = obj.color(self.params.border_color)

        return self.border
