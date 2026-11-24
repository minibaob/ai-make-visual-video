#!/usr/bin/env python3
"""Pixel check: r=1.0u circle must render ~240px wide, centred (540, 960)."""
from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30
config.frame_height = 8
config.frame_width = 4.5
config.background_color = "#0A0A0F"


class PixelTest(Scene):
    def construct(self):
        self.add(Circle(radius=1.0, color="#58C4DD", stroke_width=8))
