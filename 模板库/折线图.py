# -*- coding: utf-8 -*-
"""
【图模板 1】折线图 —— 单折线 + 关键节点标注 + 区间阴影
适用场景：时间序列主图（GDP 变化、人口增长、指标趋势）
用法：
    1. 改「① 数据区」：换成你的 x, y
    2. 改「② 图形设置区」：标题/坐标轴/标注点/填充区间
    3. 直接运行本文件，输出到 figures/
依赖：同目录 theme.py（公共色板/字体/保存工具），运行前保持在同一目录
参考样图：素材/参考_折线图.png（复刻目标效果）
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from theme import use_theme, C_BLUE, _grid, save_fig


def line_chart(ax, x, y, *,
               color=C_BLUE, lw=3, label=None,
               xlabel="", ylabel="", title="",
               annotate=None,        # (i0, i1): 标注开始/结束两个节点（含数值+虚线）
               fill=None,            # (i0, i1): 两节点之间填充阴影
               y_fmt=None,           # Y轴数值格式化函数，如 lambda v: f"{v/1e8:.1f}亿"
               x_ticks=None,         # 自定义 X 轴刻度，如 np.arange(2000, 2015)
               legend_loc="best"):
    """单折线 + 关键节点标注 + 区间阴影。
    annotate=(i0, i1)：在第 i0/i1 个点画白色描边散点 + 垂直虚线 + 数值文字。
    fill=(i0, i1)    ：填充这两点之间的区域（低透明度）。
    """
    ax.plot(x, y, color=color, lw=lw, zorder=5, label=label)

    if fill is not None:
        i0, i1 = fill
        ax.fill_between(x[i0:i1 + 1], y[i0:i1 + 1], color=color, alpha=0.1, zorder=2)

    if annotate is not None:
        for i in annotate:
            ax.scatter(x[i], y[i], marker="o", s=100, color=color,
                       edgecolors="white", linewidths=3, zorder=6)
            ax.plot([x[i], x[i]], [0, y[i]], ls="--", lw=1.2, color=color, alpha=0.7, zorder=3)
            txt = f"{y[i]:,.1f}" if y_fmt is None else y_fmt(y[i])
            dx = (x[-1] - x[0]) * 0.02          # 文字左右错开，避免遮挡
            ax.text(x[i] + dx, y[i], txt, color=color, fontweight="bold",
                    ha="left", va="bottom")

    if y_fmt is not None:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: y_fmt(v)))
    if x_ticks is not None:
        ax.set_xticks(x_ticks)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if label is not None:
        ax.legend(loc=legend_loc)
    _grid(ax)


if __name__ == "__main__":
    use_theme("journal")                 # 全队统一主题：'journal' 或 'minimal'

    # ① 数据区（替换成你的数据）
    x = np.arange(2000, 2015)
    y = np.cumprod(1 + np.linspace(0.08, 0.13, 15)) * 10   # 模拟 GDP 增长

    # ② 图形设置区
    fig, ax = plt.subplots(figsize=(8, 5))
    line_chart(ax, x, y,
               xlabel="年份 (年)", ylabel="GDP (万亿元)",
               title="图1 某地区 GDP 增长趋势",
               annotate=(0, 14),        # 标注第 0 和第 14 个点
               fill=(0, 14),            # 填充两点之间的阴影
               y_fmt=lambda v: f"{v:,.1f}",
               x_ticks=np.arange(2000, 2015, 2))
    save_fig(fig, "图1_GDP趋势")
    plt.show()
