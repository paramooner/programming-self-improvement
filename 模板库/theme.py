# -*- coding: utf-8 -*-
"""
theme.py —— 数模作图模板库：全局色板与主题加载
用法：
    from theme import COLORS, use_theme
    use_theme('journal')   # 或 'minimal'，全队统一选一套
"""
from pathlib import Path
import inspect

import matplotlib.pyplot as plt
from cycler import cycler
# ================= 统一色板：Okabe-Ito 色盲友好 8 色 =================
# 取色规则：按顺序取用；基准线/无效假设线用 GREY 虚线；阴影用同系色 alpha=0.1~0.15
COLORS = [
    "#0072B2",  # 蓝   （主色调，默认第一根线）
    "#E69F00",  # 橙
    "#009E73",  # 绿
    "#D55E00",  # 红
    "#CC79A7",  # 紫
    "#56B4E9",  # 天蓝
    "#F0E442",  # 黄
    "#999999",  # 灰   （基准线专用）
]
C_BLUE, C_ORANGE, C_GREEN, C_RED = COLORS[0], COLORS[1], COLORS[2], COLORS[3]
C_PURPLE, C_SKY, C_YELLOW, C_GREY = COLORS[4], COLORS[5], COLORS[6], COLORS[7]

# 常用语义色
C_BASELINE = "#999999"   # 基准线 / 无效假设线
C_FILL = "#b0d0e8"       # 区间阴影（浅蓝），配合 alpha=0.1~0.15

# 基准线样式
BASELINE_KW = dict(color=C_BASELINE, ls="--", lw=1.5, alpha=0.6, zorder=1)

# 样式文件所在目录
_STYLE_DIR = Path(__file__).resolve().parent

# 当前主题（由 use_theme 设置）
_THEME = {"name": "journal"}

def grid_mode() -> str:
    """返回当前主题的网格模式：'journal' → 双轴虚线网格；'minimal' → 仅水平网格线"""
    return "both" if _THEME["name"] == "journal" else "y"

# ================= 主题加载 =================
def use_theme(name: str = "journal"):
    """加载全局主题：'journal'（期刊风，默认）或 'minimal'（极简风）。
    全队约定统一使用同一主题，保证论文所有图风格一致。
    """
    assert name in ("journal", "minimal"), "主题只能是 'journal' 或 'minimal'"
    plt.style.use(_STYLE_DIR / f"{name}.mplstyle")
    # 统一色板（.mplstyle 文件中的 # 会被当作注释，故在此显式设置）
    plt.rcParams["axes.prop_cycle"] = cycler("color", COLORS)
    # PDF 内嵌 TrueType 字体：保证导出的 PDF 文字是矢量、可复制、缩放不糊
    plt.rcParams["pdf.fonttype"] = 42
    _THEME["name"] = name
    return name


def get_color(i: int) -> str:
    """按序号取色（循环使用色板）"""
    return COLORS[i % len(COLORS)]


# ================= 公共绘图工具 =================
def _grid(ax):
    """按当前主题画网格：journal → 双轴虚线；minimal → 仅水平线"""
    if grid_mode() == "y":
        ax.grid(axis="y")
    else:
        ax.grid(True, ls="--", alpha=0.3)


def save_fig(fig, name, dpi=300, outdir=None):
    """同时输出 PDF（排版用）和 PNG（预览用）。
    name：文件名（建议与代码文件同名，如 折线图.py → '折线图'）
    outdir：输出目录；默认 None = 自动保存到**调用方脚本所在目录**（代码与图放一起）
    """
    if outdir is None:
        frame = inspect.stack()[1]
        outdir = Path(frame.filename).resolve().parent
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.pdf")
    fig.savefig(out / f"{name}.png", dpi=dpi)
    print(f"已保存: {out / name}.pdf / .png")
    return out
