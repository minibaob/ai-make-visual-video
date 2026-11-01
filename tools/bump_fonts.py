"""把所有动画 HTML 里 ctx.font 的字号沿字号阶梯上移两档。

只替换 `Npx "JetBrains Mono"` 里的数字，坐标、线宽、颜色一律不动。
原文件备份到 tools/.fontbak/
"""

import re
import shutil
from pathlib import Path

ROOT = Path(r"D:\workbuddy\2026-10-30-21-55-59")
BAK = ROOT / "tools" / ".fontbak"
STEPS = 2

PAT = re.compile(r'(\d+)px(\s*"JetBrains Mono")')


def ladder_from(texts):
    return sorted({int(m.group(1)) for t in texts for m in PAT.finditer(t)})


def main():
    files = sorted(ROOT.glob("ch*.html")) + sorted(ROOT.glob("topic*.html"))
    files.append(ROOT / "derivative-tangent.html")
    files = [f for f in files if f.exists()]

    texts = [f.read_text(encoding="utf-8") for f in files]
    ladder = ladder_from(texts)
    print("字号阶梯:", ladder)

    BAK.mkdir(parents=True, exist_ok=True)
    index = {v: i for i, v in enumerate(ladder)}

    for f, text in zip(files, texts):
        if not (BAK / f.name).exists():
            shutil.copy2(f, BAK / f.name)

        def bump(m):
            v = int(m.group(1))
            i = min(index[v] + STEPS, len(ladder) - 1)
            return f"{ladder[i]}px{m.group(2)}"

        new, n = PAT.subn(bump, text)
        f.write_text(new, encoding="utf-8")
        print(f"{f.name:26s} {n:3d} 处 → 最大字号 {ladder[-1]}px")


if __name__ == "__main__":
    main()
