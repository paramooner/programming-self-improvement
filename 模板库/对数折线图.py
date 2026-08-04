# -*- coding: utf-8 -*-
"""
【图模板 2】对数折线图 —— 多系列折线 + 对数坐标 + 垂直阴影区间
适用场景：数值跨度大的多指标时序（GDP 与各产业、价格指数等）
用法：
    1. 改「① 数据区」：x、多系列数据 Y（每行一个系列）、labels
    2. 改「② 图形设置区」：标题/坐标轴/阴影区间/对数开关
    3. 直接运行本文件，输出到 figures/
依赖：同目录 theme.py（公共色板/字体/保存工具），运行前保持在同一目录
参考样图：素材/参考_对数折线图.png（复刻目标效果）
"""
import numpy as np
import matplotlib.pyplot as plt

from theme import use_theme, C_BLUE, get_color, _grid, save_fig


def multi_line_log(ax, x, Y, labels, *,
                   xlabel="", ylabel="", title="",
                   log_y=True,           # 对数坐标开关
                   shade=None,           # (x0, x1): 垂直阴影区间（按 X 值）
                   ncol=2, legend_loc="upper left"):
    """多系列折线图。Y: (n_series, n_points)；labels 与 Y 的行一一对应。
    shade=(x0, x1)：在指定 X 区间画垂直浅色阴影，突出分析区间。
    """
    n = len(labels)
    for i in range(n):
        ax.plot(x, Y[i], label=labels[i], lw=2.5, color=get_color(i))

    if log_y:
        ax.set_yscale("log")
    if shade is not None:
        x0, x1 = shade
        ax.axvspan(x0, x1, alpha=0.1, color=C_BLUE)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc=legend_loc, ncol=ncol)
    _grid(ax)


if __name__ == "__main__":
    use_theme("journal")

    # ① 数据区（替换成你的数据；可用 pandas: Y = df[cols].values.T）
    rng = np.random.default_rng(42)
    x = np.arange(2000, 2015)
    base = np.cumprod(1 + np.linspace(0.08, 0.13, 15)) * 10   # 模拟 GDP 总量
    Y = np.array([
        base,                                                   # GDP总量
        base * 0.12 * (1 + rng.normal(0, 0.01, 15)),            # 第一产业
        base * 0.45 * (1 + rng.normal(0, 0.01, 15)),            # 第二产业
        base * 0.43 * (1 + rng.normal(0, 0.01, 15)),            # 第三产业
    ])
    labels = ["GDP总量", "第一产业", "第二产业", "第三产业"]

    # ② 图形设置区
    fig, ax = plt.subplots(figsize=(8, 5))
    multi_line_log(ax, x, Y, labels,
                   xlabel="年份 (年)", ylabel="数值 (亿元, 对数坐标)",
                   title="图2 经济指标变化趋势",
                   shade=(2005, 2008))    # 突出 2005-2008 区间
    save_fig(fig, "图2_多系列对数折线")
    plt.show()
