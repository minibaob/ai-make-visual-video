#!/usr/bin/env python3
"""Postpartum v2 images 04/05 only, matching the new-voice body proposed
2026-11-13 evening (structure varies, no parallel aphorism closings).
Images 01-03 are unchanged copies in this folder.
Output: postpartum-04.png, postpartum-05.png (2160x2880, same D3 style).
"""
import os, sys
sys.path.insert(0, "/home/hatch/workspace/xhs/postpartum")
# reuse drawing helpers by importing the original generator module would
# execute it; instead duplicate the small helper set here by exec'ing only
# the top part of the original file up to the "# ================= 01" marker.
src = open("/home/hatch/workspace/xhs/postpartum/gen_postpartum.py").read()
top = src.split("# ================= 01")[0]
ns = {"__name__": "helpers"}
exec(top, ns)
OUT = "/home/hatch/workspace/xhs/postpartum-v2"
W, H, MX, RIGHT = ns["W"], ns["H"], ns["MX"], ns["RIGHT"]
base_page, header, footer = ns["base_page"], ns["header"], ns["footer"]
title_block, subtitle, hairline = ns["title_block"], ns["subtitle"], ns["hairline"]
item_block, scene_block = ns["item_block"], ns["scene_block"]
CARD, CARD_BD, INK, GREY, FAINT = ns["CARD"], ns["CARD_BD"], ns["INK"], ns["GREY"], ns["FAINT"]
bold, reg = ns["bold"], ns["reg"]
ImageDraw = ns["ImageDraw"]

# ================= 04 现在回头看（新版正文口径） =================
im, d = base_page(4)
header(d, "现在回头看", 4)
y = title_block(d, [
    [("现在回头看，", INK)],
    [("全是对的", ns["RED"])],
])
y = subtitle(d, ["当时是真嫌她烦。"], y + 55)
hairline(d, y + 55)
y += 80
y = item_block(d, y, 1, "饭按时吃好了", [
    "身体先有劲了，气色、头发才慢慢回来。",
    "也没吃什么补品，就是先把饭吃好。",
])
hairline(d, y + 35)
y += 70
y = item_block(d, y, 2, "每天出门走走", [
    "晒了太阳、走了路，晚上反而好睡一点。",
])
hairline(d, y + 35)
y += 70
y = item_block(d, y, 3, "跟着孩子睡", [
    "觉补回来，白天不用靠硬撑了。",
])
cy0 = y + 70
cy1 = cy0 + 400
d.rounded_rectangle([MX, cy0, RIGHT, cy1], radius=36, fill=CARD, outline=CARD_BD, width=2)
d.text((MX + 60, cy0 + 50), "一年下来，我没吃什么特别的，也没练什么特别的。",
       font=bold(64), fill=INK)
d.text((MX + 60, cy0 + 150), "就是饭按时吃、每天出门走、孩子睡了就睡。",
       font=bold(64), fill=INK)
d.text((MX + 60, cy0 + 265), "身体是这样一点点养回来的。",
       font=reg(60), fill=GREY)
footer(d, "全是对的", 4)
im.save(f"{OUT}/postpartum-04.png")
print("04 saved")

# ================= 05 收尾（新版正文口径） =================
im, d = base_page(5)
header(d, "一年下来", 5)
y = title_block(d, [
    [("身体是这样", INK)],
    [("一点点养回来的", ns["RED"])],
])
y = subtitle(d, ["饭按时吃、每天出门走、孩子睡了就睡。"], y + 55)
hairline(d, y + 55)
y += 105
recap = [
    ("01", "按时吃饭，不节食", "先把身体吃回来"),
    ("02", "每天出门走走", "总闷在家里更没劲"),
    ("03", "孩子睡了就跟着睡", "该睡就睡"),
    ("04", "一年下来", "就是这三件小事"),
]
for num, head, tail in recap:
    d.text((MX, y), num, font=reg(64), fill=FAINT)
    d.text((MX + 150, y - 6), f"{head}，{tail}", font=bold(76), fill=INK)
    y += 168
    if num != "04":
        hairline(d, y - 12)
hairline(d, y - 12)
cy0 = y + 55
cy1 = cy0 + 430
d.rounded_rectangle([MX, cy0, RIGHT, cy1], radius=36, fill=CARD, outline=CARD_BD, width=2)
d.text((MX + 60, cy0 + 60), "你生完孩子第一年，家里人逼你做过什么？", font=bold(76), fill=INK)
d.text((MX + 60, cy0 + 165), "评论区说说，我下一篇接着拆。", font=bold(76), fill=INK)
d.text((MX + 60, cy0 + 290), "身体是这样一点点养回来的。",
       font=reg(54), fill=GREY)
d.text((MX, cy1 + 55),
       "本文为个人经历与公开健康常识整理，不构成医疗建议，身体不适请就医。",
       font=reg(50), fill=FAINT)
footer(d, "收藏 · 转给刚生完孩子的她 · 关注看下一篇", 5)
im.save(f"{OUT}/postpartum-05.png")
print("05 saved")
print("done")
