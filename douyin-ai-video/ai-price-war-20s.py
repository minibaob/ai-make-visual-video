#!/usr/bin/env python3
"""Douyin AI video 01 - price war arithmetic. 1080x1920, ~20s, 30fps.

Topic: Claude Fable 5.2 scores 65 (No.1) but costs $26.54 per benchmark set;
GPT-6.2 Astra scores 62 and costs $4.00; both charge the same $8 in / $40 out
per million tokens. Numbers verified by the main agent, 2026-11-26.

Storyboard (6 sections, 20.1s total). Voiceover offsets in the mix:
  S1 0.20s (3.816s), S2 4.45s (3.384s), S3 8.15s (2.832s),
  S4 11.35s (3.048s), S5 14.75s (2.616s), S6 17.75s (2.424s).
  A 4.2 / B 3.7 / C 3.2 / D 3.4 / E 3.0 / F 2.6 = 20.1s.
No follow CTA, no capsule inside the video. On-screen text only + voiceover.
Safe zones: keep content between y -2.4 and y 3.0.

Run: ~/workspace/venvs/manim/bin/manim render --format=mp4 \
       --resolution 1080,1920 --fps 30 ai-price-war-20s.py AIPriceWar
NOTE: do NOT pass -qm/-ql/-qh (forces 1280x720 and letterboxes).
config.frame_width = 4.5 is required for a true 4.5 x 8 portrait frame
(240 px per unit). All text goes through fit_width() (max 4.2u).
LaTeX is NOT installed on this VM: plain Text + Unicode only.
"""
import numpy as np
from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30
config.frame_height = 8
config.frame_width = 4.5
config.background_color = "#0A0A0F"

CYAN = "#58C4DD"
YELLOW = "#FFD93D"
WHITE = "#F8FAFC"
GREY = "#8A94A6"
DARK_CARD = "#11141F"


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


def hbar(x0, y, length, color, height=0.34):
    """Horizontal bar from x0, growing right, centred vertically at y."""
    return Rectangle(width=length, height=height, color=color,
                     fill_color=color, fill_opacity=1, stroke_width=0
                     ).move_to(np.array([x0 + length / 2, y, 0.0]))


class AIPriceWar(Scene):
    def construct(self):
        print("building AI price-war scene...", flush=True)
        bg = dot_grid()

        # ---- section A: hook ----
        big_price = fit_width(Text("$26.54", font_size=72, color=YELLOW))
        big_price.move_to(np.array([0.0, 0.70, 0.0]))
        sub_a = fit_width(Text("同样一套题，第一名花了", font_size=30,
                               color=WHITE))
        sub_a.move_to(np.array([0.0, -0.40, 0.0]))

        # ---- section B: score bars (65 vs 62) ----
        title_b = fit_width(Text("分数，几乎一样", font_size=30, color=WHITE))
        title_b.move_to(np.array([0.0, 2.70, 0.0]))
        lab_b1 = fit_width(Text("Claude Fable 5.2", font_size=20, color=GREY))
        lab_b1.move_to(np.array([-1.90, 1.75, 0.0])).set_x(-1.90, direction=LEFT)
        bar_b1 = hbar(-1.90, 1.10, 3.53, CYAN)
        num_b1 = fit_width(Text("65", font_size=30, color=CYAN))
        num_b1.move_to(np.array([0.0, 1.10, 0.0])).set_x(1.71, direction=LEFT)
        lab_b2 = fit_width(Text("GPT-6.2 Astra", font_size=20, color=GREY))
        lab_b2.move_to(np.array([-1.90, 0.55, 0.0])).set_x(-1.90, direction=LEFT)
        bar_b2 = hbar(-1.90, -0.10, 3.37, GREY)
        num_b2 = fit_width(Text("62", font_size=30, color=GREY))
        num_b2.move_to(np.array([0.0, -0.10, 0.0])).set_x(1.55, direction=LEFT)
        cap_b = fit_width(Text("只差 3 分", font_size=26, color=WHITE))
        cap_b.move_to(np.array([0.0, -1.30, 0.0]))
        group_b = VGroup(title_b, lab_b1, bar_b1, num_b1, lab_b2, bar_b2,
                         num_b2, cap_b)

        # ---- section C: same unit price ----
        price_l = fit_width(Text("$8 / $40", font_size=32, color=WHITE))
        price_l.move_to(np.array([-1.28, 0.50, 0.0]))
        eq = fit_width(Text("=", font_size=48, color=YELLOW))
        eq.move_to(np.array([0.0, 0.50, 0.0]))
        price_r = fit_width(Text("$8 / $40", font_size=32, color=WHITE))
        price_r.move_to(np.array([1.28, 0.50, 0.0]))
        lab_c1 = fit_width(Text("Claude", font_size=18, color=GREY))
        lab_c1.move_to(np.array([-1.28, -0.15, 0.0]))
        lab_c2 = fit_width(Text("GPT", font_size=18, color=GREY))
        lab_c2.move_to(np.array([1.28, -0.15, 0.0]))
        cap_c = fit_width(Text("单价明明一样", font_size=30, color=WHITE))
        cap_c.move_to(np.array([0.0, -1.20, 0.0]))
        group_c = VGroup(price_l, eq, price_r, lab_c1, lab_c2, cap_c)

        # ---- section D: cost bars, the visual climax ----
        title_d = fit_width(Text("花多少，差 6.6 倍", font_size=30, color=WHITE))
        title_d.move_to(np.array([0.0, 2.70, 0.0]))
        lab_d1 = fit_width(Text("Claude Fable 5.2", font_size=20, color=GREY))
        lab_d1.move_to(np.array([-1.90, 1.75, 0.0])).set_x(-1.90, direction=LEFT)
        bar_d1 = hbar(-1.90, 1.10, 2.70, YELLOW)
        num_d1 = fit_width(Text("$26.54", font_size=24, color=YELLOW))
        num_d1.move_to(np.array([0.0, 1.10, 0.0])).set_x(0.88, direction=LEFT)
        lab_d2 = fit_width(Text("GPT-6.2 Astra", font_size=20, color=GREY))
        lab_d2.move_to(np.array([-1.90, 0.55, 0.0])).set_x(-1.90, direction=LEFT)
        bar_d2 = hbar(-1.90, -0.10, 0.45, CYAN)
        num_d2 = fit_width(Text("$4.00", font_size=28, color=CYAN))
        num_d2.move_to(np.array([0.0, -0.10, 0.0])).set_x(-1.37, direction=LEFT)
        big66 = fit_width(Text("6.6 倍", font_size=44, color=YELLOW))
        big66.move_to(np.array([0.0, -1.30, 0.0]))
        cap_d = fit_width(Text("贵就贵在它话太多", font_size=24, color=GREY))
        cap_d.move_to(np.array([0.0, -1.95, 0.0]))
        group_d = VGroup(title_d, lab_d1, bar_d1, num_d1, lab_d2, bar_d2,
                         num_d2, big66, cap_d)

        # ---- section E: source ----
        recap_e = fit_width(Text("65 分 · $26.54　|　62 分 · $4.00",
                                 font_size=24, color=GREY))
        recap_e.move_to(np.array([0.0, 0.90, 0.0]))
        src1 = fit_width(Text("数据：Artificial Analysis 智力指数",
                              font_size=22, color=GREY))
        src1.move_to(np.array([0.0, 0.10, 0.0]))
        src2 = fit_width(Text("（第三方榜单），2026 年 11 月",
                              font_size=22, color=GREY))
        src2.move_to(np.array([0.0, -0.40, 0.0]))
        group_e = VGroup(recap_e, src1, src2)

        # ---- section F: closing ----
        take1 = fit_width(Text("三分，", font_size=44, color=YELLOW))
        take1.move_to(np.array([0.0, 0.60, 0.0]))
        take2 = fit_width(Text("多花二十二块", font_size=44, color=YELLOW))
        take2.move_to(np.array([0.0, -0.10, 0.0]))
        group_f = VGroup(take1, take2)

        # ---- A: 0-4.2s hook ----
        self.add(bg)
        self.play(GrowFromCenter(big_price), FadeIn(sub_a, shift=UP * 0.1),
                  run_time=0.5, rate_func=smooth)
        self.wait(3.7)

        # ---- B: 4.2-7.9s score bars ----
        self.play(FadeOut(big_price), FadeOut(sub_a),
                  FadeIn(group_b, shift=UP * 0.1),
                  run_time=0.5, rate_func=smooth)
        self.wait(3.2)

        # ---- C: 7.9-11.1s same unit price ----
        self.play(FadeOut(group_b), FadeIn(group_c, shift=UP * 0.1),
                  run_time=0.5, rate_func=smooth)
        self.wait(2.7)

        # ---- D: 11.1-14.5s cost bars ----
        self.play(FadeOut(group_c), FadeIn(group_d, shift=UP * 0.1),
                  run_time=0.5, rate_func=smooth)
        self.wait(2.9)

        # ---- E: 14.5-17.5s source ----
        self.play(FadeOut(group_d), FadeIn(group_e, shift=UP * 0.1),
                  run_time=0.5, rate_func=smooth)
        self.wait(2.5)

        # ---- F: 17.5-20.1s closing freeze ----
        self.play(FadeOut(group_e), FadeIn(group_f, shift=UP * 0.2),
                  run_time=0.5, rate_func=smooth)
        self.wait(2.1)
        print("scene done (20.1s)", flush=True)
