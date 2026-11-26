#!/usr/bin/env python3
"""Font smoke test: render one frame with the same Text calls as the
price-war scene, to check Chinese renders before the full render."""
from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30
config.frame_height = 8
config.frame_width = 4.5
config.background_color = "#0A0A0F"


class FontTest(Scene):
    def construct(self):
        a = Text("$26.54", font_size=72, color="#FFD93D")
        a.move_to(np.array([0.0, 0.70, 0.0]))
        b = Text("同样一套题，第一名花了", font_size=30, color="#F8FAFC")
        b.move_to(np.array([0.0, -0.40, 0.0]))
        c = Text("数据：Artificial Analysis 智力指数", font_size=22,
                 color="#8A94A6")
        c.move_to(np.array([0.0, -1.20, 0.0]))
        self.add(a, b, c)
        self.wait(0.2)
