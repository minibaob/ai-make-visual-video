#!/usr/bin/env python3
"""Taylor formula (sin x) - Douyin video, 30s, 1080x1920, 30fps.

Concept (perform it, don't lecture it): sin(x) as a curve, then its Taylor
polynomials of degree 1, 3, 5, 7 snapping onto the curve near x=0, each one
hugging further out. Frame 0 already shows the sin curve with the degree-1
polynomial on it. Ends with the full formula + one plain takeaway line.

Math (exact, verified 2026-11-18):
  sin x = x - x^3/3! + x^5/5! - x^7/7!
        = x - x^3/6 + x^5/120 - x^7/5040
  P1 = x
  P3 = x - x^3/6
  P5 = x - x^3/6 + x^5/120
  P7 = x - x^3/6 + x^5/120 - x^7/5040
Plot ranges chosen so every curve stays inside the axes box:
  P1 plotted on [-1.6, 1.6] (y = x would leave the box beyond that),
  P3 plotted on [-2.9, 2.9] (P3(3.0) = -1.5, P3(3.1) < -1.6, out of box),
  P5, P7 plotted on the full [-3.6, 3.6] (stay within y in [-1.6, 1.6]).

Storyboard (6 sections x 5.0 s = 30.000 s):
  0-5s   hook: axes + sin (blue) + P1 line (yellow) at frame 0;
         "一条直线，贴不住 sin x / 多项式可以，一项一项往上加"
  5-10s  P1 dims, P3 (green) draws on, hugging to ~|x| 1.5;
         caption "x - x^3/6 / 三次，贴得更远了"
  10-15s P5 (red) draws on, hugging to ~|x| 2.3;
         caption "x - x^3/6 + x^5/120 / 五次，再远一点"
  15-20s P7 (white) draws on, hugging to ~|x| 3.0;
         caption "x - x^3/6 + x^5/120 - x^7/5040 / 七次，几乎分不出来了"
  20-25s P1/P3/P5 fade out (sin + P7 stay); full formula written;
         caption "这就是泰勒公式"
  25-30s closing freeze: "再复杂的曲线，都是多项式拼出来的" + formula
No follow CTA, no capsule inside. Narration: 6 segments, one per 5 s window.
Safe zones: top 240 px (y <= 3.0), bottom 380 px (y >= -2.417).

Run: ~/workspace/venvs/manim/bin/manim render --format=mp4 \
       --resolution 1080,1920 --fps 30 taylor-manim-30s.py TaylorManim
NOTE: do NOT pass -qm/-ql/-qh (forces 1280x720 and letterboxes).
config.frame_width = 4.5 is required for a true 4.5 x 8 portrait frame
(240 px per unit). All text goes through fit_width() (max 4.2u).
"""
import math

import numpy as np
from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30
config.frame_height = 8
config.frame_width = 4.5
config.background_color = "#0A0A0F"

BLUE = "#58C4DD"
YELLOW = "#FFD93D"
RED = "#FF6B6B"
GREEN = "#83C167"
WHITE = "#F8FAFC"
GREY = "#8A94A6"

AX_C = np.array([0.0, 0.62, 0.0])   # axes centre
X_MIN, X_MAX = -3.6, 3.6


def fit_width(mob, max_w=4.2):
    """Scale down if wider than the narrow vertical frame; print the check."""
    if mob.width > max_w:
        mob.scale(max_w / mob.width)
    print(f"  width check: {mob.width:.2f} units (max {max_w})", flush=True)
    return mob


def dot_grid():
    dots = VGroup(*[
        Dot(point=np.array([x, y, 0.0]), radius=0.014, color="#181B28",
            fill_opacity=1)
        for x in np.arange(-2.1, 2.11, 0.375)
        for y in np.arange(-3.8, 3.81, 0.375)
    ])
    return dots


def p1(x):
    return x


def p3(x):
    return x - x ** 3 / 6.0


def p5(x):
    return x - x ** 3 / 6.0 + x ** 5 / 120.0


def p7(x):
    return x - x ** 3 / 6.0 + x ** 5 / 120.0 - x ** 7 / 5040.0


# exactness printout (also guards the script against a typo)
for _x in (0.5, 1.0, 2.0):
    print(f"  check x={_x}: sin={math.sin(_x):.6f} "
          f"P1={p1(_x):.6f} P3={p3(_x):.6f} P5={p5(_x):.6f} "
          f"P7={p7(_x):.6f}", flush=True)


class TaylorManim(Scene):
    def construct(self):
        print("building taylor scene...", flush=True)

        bg = dot_grid()

        ax = Axes(
            x_range=[X_MIN, X_MAX, 1],
            y_range=[-1.6, 1.6, 0.5],
            x_length=4.0,
            y_length=2.5,
            axis_config={"color": GREY, "stroke_width": 2},
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": False},
            tips=False,
        ).move_to(AX_C)
        x_lab = Text("x", font_size=22, color=GREY)
        x_lab.move_to(ax.coords_to_point(X_MAX + 0.25, 0))
        y_lab = Text("y", font_size=22, color=GREY)
        # right of the axis, well below the subtitle: centred above the
        # axis it collides with the subtitle, and on the axis it would
        # sit on the axis line itself. (0.30, 1.30) is clear of both.
        y_lab.move_to(ax.coords_to_point(0.30, 1.30))
        pi_lab = Text("π", font_size=20, color=GREY)
        pi_lab.move_to(ax.coords_to_point(math.pi, -0.28))
        mpi_lab = Text("-π", font_size=20, color=GREY)
        mpi_lab.move_to(ax.coords_to_point(-math.pi, -0.28))
        axes_group = VGroup(ax, x_lab, y_lab, pi_lab, mpi_lab)

        sin_curve = ax.plot(lambda x: math.sin(x), x_range=[X_MIN, X_MAX, 0.02],
                            color=BLUE, stroke_width=6)
        p1_line = ax.plot(p1, x_range=[-1.6, 1.6, 0.02],
                          color=YELLOW, stroke_width=5)
        p3_curve = ax.plot(p3, x_range=[-2.9, 2.9, 0.02],
                           color=GREEN, stroke_width=5)
        p5_curve = ax.plot(p5, x_range=[X_MIN, X_MAX, 0.02],
                           color=RED, stroke_width=5)
        p7_curve = ax.plot(p7, x_range=[X_MIN, X_MAX, 0.02],
                           color=WHITE, stroke_width=5)

        # ---- hook text (fades in over 0.33s; figure is there at frame 0) ----
        title = fit_width(Text("一条直线，贴不住 sin x", font_size=38, color=WHITE))
        title.move_to(np.array([0.0, 2.78, 0.0]))
        subtitle = fit_width(Text("多项式可以，一项一项往上加", font_size=22,
                                  color=GREY))
        subtitle.move_to(np.array([0.0, 2.30, 0.0]))

        # ---- caption band + captions (slots upper -1.55 / lower -2.05) ----
        band = Rectangle(width=4.5, height=1.15, color="#0A0A0F",
                         stroke_width=0, fill_color="#0A0A0F",
                         fill_opacity=0.78).move_to(np.array([0.0, -1.80, 0.0]))

        def caption(formula_text, note, fcolor):
            # NOTE 2026-11-18: texlive is NOT installed on this VM any more
            # (lost in a VM replacement; `latex` binary missing), so the
            # formulas use plain Text with Unicode superscripts (x^3, x^5,
            # x^7, -, ~) instead of MathTex. Glyphs verified rendering
            # correctly (glyph test 2026-11-18); fit_width keeps them in frame.
            f = fit_width(Text(formula_text, font_size=34, color=fcolor))
            f.move_to(np.array([0.0, -1.55, 0.0]))
            n = fit_width(Text(note, font_size=28, color=GREY))
            n.move_to(np.array([0.0, -2.05, 0.0]))
            return VGroup(f, n)

        cap_b = caption("x − x³/6", "三次，贴得更远了", GREEN)
        cap_c = caption("x − x³/6 + x⁵/120",
                        "五次，再远一点", RED)
        cap_d = caption("x − x³/6 + x⁵/120 − x⁷/5040",
                        "七次，几乎分不出来了", WHITE)
        formula_full = fit_width(Text(
            "sin x ≈ x − x³/6 + x⁵/120 − x⁷/5040",
            font_size=30, color=YELLOW))
        formula_full.move_to(np.array([0.0, -1.55, 0.0]))
        note_e = fit_width(Text("这就是泰勒公式", font_size=30, color=WHITE))
        note_e.move_to(np.array([0.0, -2.05, 0.0]))

        # ---- closing freeze ----
        take1 = fit_width(Text("再复杂的曲线，", font_size=44, color=WHITE))
        take1.move_to(np.array([0.0, 0.85, 0.0]))
        take2 = fit_width(Text("都是多项式拼出来的", font_size=44, color=YELLOW))
        take2.move_to(np.array([0.0, 0.15, 0.0]))
        formula_small = fit_width(Text(
            "sin x ≈ x − x³/6 + x⁵/120 − x⁷/5040",
            font_size=26, color=GREEN))
        formula_small.move_to(np.array([0.0, -0.75, 0.0]))

        # ---- frame 0: axes + sin + P1 already on screen ----
        self.add(bg, axes_group, sin_curve, p1_line)

        # ---- A: 0-5s hook ----
        self.play(FadeIn(title, shift=UP * 0.1),
                  FadeIn(subtitle, shift=UP * 0.1),
                  run_time=0.33, rate_func=smooth)
        self.wait(4.67)

        # ---- B: 5-10s P3 snaps on ----
        p1_dim = p1_line.copy().set_color(GREY).set_opacity(0.35)
        self.play(Transform(p1_line, p1_dim), run_time=0.5, rate_func=smooth)
        self.play(Create(p3_curve), FadeIn(band), FadeIn(cap_b),
                  run_time=1.5, rate_func=smooth)
        self.wait(3.0)

        # ---- C: 10-15s P5 snaps on ----
        self.play(FadeOut(cap_b), run_time=0.4)
        self.play(Create(p5_curve), FadeIn(cap_c),
                  run_time=1.5, rate_func=smooth)
        self.wait(3.1)

        # ---- D: 15-20s P7 snaps on ----
        self.play(FadeOut(cap_c), run_time=0.4)
        self.play(Create(p7_curve), FadeIn(cap_d),
                  run_time=1.5, rate_func=smooth)
        self.wait(3.1)

        # ---- E: 20-25s formula ----
        self.play(FadeOut(p1_line), FadeOut(p3_curve), FadeOut(p5_curve),
                  FadeOut(cap_d), run_time=0.5)
        self.play(Write(formula_full), run_time=2.0)
        self.play(FadeIn(note_e), run_time=0.5)
        self.wait(2.0)

        # ---- F: 25-30s closing freeze ----
        self.play(FadeOut(axes_group), FadeOut(sin_curve), FadeOut(p7_curve),
                  FadeOut(band), FadeOut(formula_full), FadeOut(note_e),
                  FadeOut(title), FadeOut(subtitle), run_time=0.6)
        self.play(FadeIn(take1, shift=UP * 0.2), FadeIn(take2),
                  FadeIn(formula_small), run_time=0.9)
        self.wait(3.5)
        print("scene done (30.000s)", flush=True)
