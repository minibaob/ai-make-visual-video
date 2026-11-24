#!/usr/bin/env python3
"""Birthday paradox - Douyin video, 20s, 1080x1920, 30fps.

Concept (perform it, don't lecture it): 23 people in a room, two share a
birthday - and that is not luck, it is arithmetic. Frame 0 already shows
23 dots + the hook line. Dots arrive one by one, the pair count explodes
to 253, then the probability curve climbs past 50% at 23 people.

Math (exact, verified 2026-11-23, 365-day year):
  P(n) = 1 - prod((365-i)/365 for i in range(n))
  n=10 -> 11.7% (~12%), n=23 -> 50.7% (over half), n=40 -> 89.1% (~89%),
  n=70 -> 99.9%.  C(23,2) = 253 pairs, C(70,2) = 2415 pairs.

Storyboard (4 sections x 5.0 s = 20.000 s):
  0-5s   hook: 23 dots + "23 个人里，居然有两个人同一天生日" at frame 0;
         at ~2.5s two dots flash red + rings + "撞上了！"
  5-10s  "人一个一个进来": dots pop in one by one, then "253 对" lands;
         caption "机会不是 23 次，是 253 次"
  10-15s probability curve draws 0->70 with markers 23人 50.7% / 40人 89% /
         70人 99.9%; dashed 50% line; caption "不是巧合，是配对太多了"
  15-20s closing freeze: "23 个人，过半会撞上" + "生日撞车，一点都不稀奇"
         (last ~3.5s static)
No follow CTA, no capsule inside, no voiceover. On-screen text only.
Safe zones: top 240 px (y <= 3.0), bottom 380 px (y >= -2.417).

Run: ~/workspace/venvs/manim/bin/manim render --format=mp4 \
       --resolution 1080,1920 --fps 30 birthday-manim-20s.py BirthdayManim
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

# exactness printout (also guards the script against a typo)
for _n in (10, 23, 40, 70):
    _p = 1 - math.prod((365 - i) / 365 for i in range(_n))
    print(f"  check n={_n}: P={_p * 100:.1f}%  pairs={_n * (_n - 1) // 2}",
          flush=True)


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


def people_dots(center_y):
    """23 dots (people), 5 cols x 5 rows minus 2, centred at (0, center_y)."""
    pts = []
    for r in range(5):
        for c in range(5):
            if r == 4 and c >= 3:
                continue
            pts.append(np.array([-1.24 + c * 0.62,
                                 center_y + 1.24 - r * 0.62, 0.0]))
    return VGroup(*[Dot(point=p, radius=0.09, color=BLUE,
                         fill_opacity=1) for p in pts]), pts


class BirthdayManim(Scene):
    def construct(self):
        print("building birthday scene...", flush=True)
        bg = dot_grid()

        # ---- section A objects ----
        dots_a, pts_a = people_dots(0.35)
        title1 = fit_width(Text("23 个人里，", font_size=44, color=WHITE))
        title1.move_to(np.array([0.0, 2.80, 0.0]))
        title2 = fit_width(Text("居然有两个人同一天生日", font_size=28,
                                color=YELLOW))
        title2.move_to(np.array([0.0, 2.20, 0.0]))
        hit = fit_width(Text("撞上了！", font_size=32, color=RED))
        hit.move_to(np.array([0.0, -1.60, 0.0]))
        pair_idx = (11, 12)  # two middle dots
        rings_a = VGroup(*[
            Circle(radius=0.20, color=YELLOW, stroke_width=5).move_to(pts_a[i])
            for i in pair_idx
        ])

        # ---- section B objects ----
        top_b = fit_width(Text("人一个一个进来", font_size=30, color=WHITE))
        top_b.move_to(np.array([0.0, 2.80, 0.0]))
        big253 = fit_width(Text("253 对", font_size=56, color=YELLOW))
        big253.move_to(np.array([0.0, -1.50, 0.0]))
        cap_b = fit_width(Text("机会不是 23 次，是 253 次", font_size=24,
                               color=GREY))
        cap_b.move_to(np.array([0.0, -2.05, 0.0]))

        # ---- section C objects ----
        title_c = fit_width(Text("人一多，概率直接起飞", font_size=30,
                                 color=WHITE))
        title_c.move_to(np.array([0.0, 2.85, 0.0]))
        cap_c = fit_width(Text("不是巧合，是配对太多了", font_size=26,
                               color=GREY))
        cap_c.move_to(np.array([0.0, -1.95, 0.0]))
        ax = Axes(
            x_range=[0, 70, 10],
            y_range=[0, 100, 20],
            x_length=3.8,
            y_length=2.9,
            axis_config={"color": GREY, "stroke_width": 2},
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": False},
            tips=False,
        ).move_to(np.array([0.0, 0.35, 0.0]))
        x_lab = Text("人数", font_size=20, color=GREY)
        x_lab.move_to(ax.coords_to_point(68, -9))
        y_lab = Text("%", font_size=20, color=GREY)
        y_lab.move_to(ax.coords_to_point(-4, 104))
        p50_line = DashedLine(
            ax.coords_to_point(0, 50), ax.coords_to_point(70, 50),
            color=GREY, stroke_width=2, dash_length=0.12)
        p50_lab = Text("50%", font_size=20, color=GREY)
        p50_lab.move_to(ax.coords_to_point(4, 44))
        probs = [100 * (1 - math.prod((365 - i) / 365 for i in range(n)))
                 for n in range(71)]
        curve_pts = [ax.coords_to_point(n, probs[n]) for n in range(71)]
        curve = (VMobject().set_points_as_corners(curve_pts)
                 .set_color(GREEN).set_stroke(width=6))

        def marker(n, color):
            m = Dot(ax.coords_to_point(n, probs[n]), radius=0.07,
                    color=color, fill_opacity=1)
            return m

        m23 = marker(23, YELLOW)
        lab23 = fit_width(Text("23人 50.7%", font_size=22, color=YELLOW))
        lab23.move_to(ax.coords_to_point(23, 50.7) + np.array([-0.55, 0.32, 0]))
        m40 = marker(40, GREEN)
        lab40 = fit_width(Text("40人 89%", font_size=22, color=GREEN))
        lab40.move_to(ax.coords_to_point(40, 89.1) + np.array([-1.05, -0.45, 0]))
        m70 = marker(70, GREEN)
        lab70 = fit_width(Text("70人 99.9%", font_size=22, color=GREEN))
        lab70.move_to(ax.coords_to_point(70, 99.9) + np.array([-0.75, 0.35, 0]))
        axes_group = VGroup(ax, x_lab, y_lab, p50_line, p50_lab)

        # ---- section D objects ----
        take1 = fit_width(Text("23 个人，过半会撞上", font_size=34,
                               color=YELLOW))
        take1.move_to(np.array([0.0, 0.70, 0.0]))
        take2 = fit_width(Text("生日撞车，一点都不稀奇", font_size=25,
                               color=WHITE))
        take2.move_to(np.array([0.0, 0.00, 0.0]))

        # ---- frame 0: dots + hook text already on screen ----
        self.add(bg, dots_a, title1, title2)

        # ---- A: 0-5s hook ----
        self.wait(2.5)
        self.play(dots_a[pair_idx[0]].animate.set_color(RED),
                  dots_a[pair_idx[1]].animate.set_color(RED),
                  Create(rings_a), FadeIn(hit, shift=UP * 0.1),
                  run_time=0.5, rate_func=smooth)
        self.wait(2.0)

        # ---- B: 5-10s people arrive one by one ----
        dots_b, pts_b = people_dots(0.75)
        rings_b = VGroup(*[
            Circle(radius=0.20, color=YELLOW, stroke_width=5).move_to(pts_b[i])
            for i in pair_idx
        ])
        self.play(FadeOut(title1), FadeOut(title2), FadeOut(hit),
                  FadeOut(rings_a), FadeOut(dots_a),
                  FadeIn(top_b, shift=UP * 0.1),
                  run_time=0.5, rate_func=smooth)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots_b],
                              lag_ratio=0.12, run_time=2.8),
                  rate_func=smooth)
        self.play(dots_b[pair_idx[0]].animate.set_color(RED),
                  dots_b[pair_idx[1]].animate.set_color(RED),
                  Create(rings_b), FadeIn(big253), FadeIn(cap_b),
                  run_time=0.5, rate_func=smooth)
        self.wait(1.2)

        # ---- C: 10-15s the curve climbs ----
        self.play(FadeOut(top_b), FadeOut(dots_b), FadeOut(rings_b),
                  FadeOut(big253), FadeOut(cap_b),
                  FadeIn(title_c, shift=UP * 0.1),
                  run_time=0.5, rate_func=smooth)
        self.play(Create(ax), run_time=0.5, rate_func=smooth)
        self.play(Create(curve), run_time=2.0, rate_func=smooth)
        self.play(FadeIn(x_lab), FadeIn(y_lab), FadeIn(p50_line),
                  FadeIn(p50_lab), FadeIn(m23), FadeIn(lab23),
                  FadeIn(m40), FadeIn(lab40), FadeIn(m70), FadeIn(lab70),
                  FadeIn(cap_c), run_time=0.8, rate_func=smooth)
        self.wait(1.2)

        # ---- D: 15-20s closing freeze ----
        self.play(FadeOut(title_c), FadeOut(axes_group), FadeOut(curve),
                  FadeOut(m23), FadeOut(lab23), FadeOut(m40), FadeOut(lab40),
                  FadeOut(m70), FadeOut(lab70), FadeOut(cap_c),
                  run_time=0.6, rate_func=smooth)
        self.play(FadeIn(take1, shift=UP * 0.2), FadeIn(take2),
                  run_time=0.9, rate_func=smooth)
        self.wait(3.5)
        print("scene done (20.000s)", flush=True)
