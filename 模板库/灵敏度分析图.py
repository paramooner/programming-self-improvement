# -*- coding: utf-8 -*-
"""
【图模板 3】灵敏度分析图 —— 样条平滑 + 局部放大 inset + 参数区间阴影
适用场景：敏感性分析、多方案对比（国奖论文高频图）
用法：
    1. 改「① 数据区」：x、y_dict（{参数值: 曲线}）、baseline（基准线）
    2. 改「② 图形设置区」：标题/坐标轴/放大区域 zoom=(x0,x1,y0,y1)
    3. 直接运行本文件，输出到 figures/
依赖：同目录 theme.py（公共色板/字体/保存工具），运行前保持在同一目录
参考样图：素材/参考_灵敏度分析图.png（复刻目标效果）
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

from theme import use_theme, C_BLUE, BASELINE_KW, get_color, _grid, save_fig


def inset_zoom_line(ax, x, y_dict, *, baseline=None, baseline_label="基准",
                    xlabel="", ylabel="", title="",
                    fill_low=None, fill_high=None,  # 区间填充的两条曲线 key
                    zoom=None,             # (x0, x1, y0, y1): inset 放大区域
                    inset_size=(0.35, 0.30), inset_loc="lower right",
                    aspect=None):          # 画布纵横比优化（如 0.65；None=不启用）
    """在 ax 上画多曲线 + 参数区间阴影 + 局部放大子图。
    y_dict: {名称: y 序列}；baseline: 基准线 y 序列（灰色虚线）。
    中间的参数曲线加粗（lw=3），其余细线（1.5）。
    aspect：按数据范围自动设置画布纵横比（xr/yr*aspect），图比例更协调。
    """
    # --- 数据平滑（三次样条，输出300点） ---
    smooth = {}
    for k, yy in y_dict.items():
        x_new = np.linspace(x.min(), x.max(), 300)
        spl = make_interp_spline(x, np.asarray(yy, float), k=3)
        smooth[k] = (x_new, spl(x_new))
    if baseline is not None:
        x_b = np.linspace(x.min(), x.max(), 300)
        spl_b = make_interp_spline(x, np.asarray(baseline, float), k=3)
        baseline = (x_b, spl_b(x_b))

    # --- 参数区间阴影（低透明度） ---
    if fill_low is not None and fill_high is not None:
        xf, y_low = smooth[fill_low]
        _, y_high = smooth[fill_high]
        ax.fill_between(xf, y_low, y_high, color=C_BLUE, alpha=0.1, zorder=2)

    # --- 主图曲线 ---
    keys = list(y_dict.keys())
    for k in keys:
        xs, ys = smooth[k]
        is_base = (k == keys[len(keys) // 2]) and len(keys) > 2
        ax.plot(xs, ys, color=get_color(keys.index(k)),
                lw=(3 if is_base else 1.5), label=f"{k}")
    if baseline is not None:
        ax.plot(*baseline, **BASELINE_KW, label=baseline_label)

    # --- 局部放大子图 ---
    if zoom is not None:
        x0, x1, y0, y1 = zoom
        ax_ins = inset_axes(ax, width=str(int(inset_size[0] * 100)) + "%",
                            height=str(int(inset_size[1] * 100)) + "%",
                            loc=inset_loc)
        for k in keys:
            xs, ys = smooth[k]
            ax_ins.plot(xs, ys, color=get_color(keys.index(k)), lw=1.2)
        if baseline is not None:
            ax_ins.plot(*baseline, **BASELINE_KW)
        # 放大子图内同样绘制参数区间色带（信息更完整）
        if fill_low is not None and fill_high is not None:
            xf2, y_low2 = smooth[fill_low]
            _, y_high2 = smooth[fill_high]
            ax_ins.fill_between(xf2, y_low2, y_high2, color=C_BLUE, alpha=0.1, zorder=1)
        ax_ins.set_xlim(x0, x1)
        ax_ins.set_ylim(y0, y1)
        ax_ins.tick_params(labelsize=7)
        ax_ins.grid(True, alpha=0.2, ls="--")
        mark_inset(ax, ax_ins, loc1=3, loc2=4, fc="none",
                   ec="gray", lw=0.8, ls="--", alpha=0.5)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc="lower left", fontsize=9)
    _grid(ax)
    # 画布纵横比优化（来自学习笔记局部放大图.md）
    if aspect is not None:
        yr = ax.get_ylim()[1] - ax.get_ylim()[0]
        xr = ax.get_xlim()[1] - ax.get_xlim()[0]
        ax.set_aspect(xr / yr * aspect)


if __name__ == "__main__":
    use_theme("journal")

    # ① 数据区（替换成你的模型输出）
    x = np.arange(2025, 2036)
    t = x - 2024.5
    y_dict = {f"α={a:.2f}": 0.55 + (a * 0.5) * (1 - np.exp(-0.4 * t))
              for a in [0.10, 0.20, 0.30]}
    baseline = 0.5 + 0.05 * np.sin(t / 5)      # S0 基准场景

    # ② 图形设置区
    y_lo = min(y_dict["α=0.10"][-3:])
    y_hi = max(y_dict["α=0.30"][-1:]) + 0.02
    fig, ax = plt.subplots(figsize=(8, 6))
    inset_zoom_line(ax, x, y_dict, baseline=baseline,
                    xlabel="年份 (年)", ylabel="总和生育率 TFR",
                    title="图3 TFR 对意愿调整速度 α 的敏感性",
                    fill_low="α=0.10", fill_high="α=0.30",
                    zoom=(2033.3, 2034.7, y_lo, y_hi),   # 放大末尾两年
                    aspect=0.65)                          # 画布纵横比优化
    save_fig(fig, "图3_灵敏度分析")
    plt.show()
