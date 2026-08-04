# -*- coding: utf-8 -*-
"""
【图模板 4】森林图 —— 学术三线表风格（回归 OR / 效应量）
适用场景：Logit 回归结果展示、多变量效应对比
用法：
    1. 改「① 数据区」：labels、ors、ci_low、ci_high、p_vals
    2. 改「② 图形设置区」：标题、X 轴刻度
    3. 直接运行本文件，输出到 figures/
依赖：同目录 theme.py（公共色板/字体/保存工具），运行前保持在同一目录
参考样图：素材/参考_森林图.png（复刻目标效果）
"""
import numpy as np
import matplotlib.pyplot as plt

from theme import use_theme, C_BLUE, save_fig


def forest_plot(ax, labels, ors, ci_low, ci_high, p_vals=None, *,
                ref=1.0,                # 无效假设参考值
                x_ticks=None,           # 如 [0.5, 1.0, 1.5, 2.0]
                title=""):
    """学术三线表风格森林图：误差线 + 效应点 + OR(95% CI) 表 + P 值表。
    第一行数据（labels[0]）显示在最上方。
    """
    # 反转使 labels[0] 在最上；转 numpy 以便向量运算
    labels = labels[::-1]
    ors = np.asarray(ors[::-1], float)
    ci_low = np.asarray(ci_low[::-1], float)
    ci_high = np.asarray(ci_high[::-1], float)
    p_vals = p_vals[::-1] if p_vals is not None else None

    n = len(labels)
    y_pos = np.arange(n)
    or_strs = [f"{o:.3f} ({l:.3f}, {h:.3f})" for o, l, h in zip(ors, ci_low, ci_high)]

    x_var, x_or, x_pval = -0.5, 0.1, 2.2   # 三列 X 位置

    ax.errorbar(ors, y_pos, xerr=[ors - ci_low, ci_high - ors],
                fmt="o", color=C_BLUE, ecolor="black",
                elinewidth=1.5, capsize=5, capthick=1.5, markersize=8, zorder=3)

    for i in range(n):
        ax.text(x_var, i, labels[i], ha="left", va="center", fontsize=11)
        ax.text(x_or, i, or_strs[i], ha="center", va="center", fontsize=11)
        if p_vals is not None:
            ax.text(x_pval, i, p_vals[i], ha="right", va="center", fontsize=11)

    header_y = n + 0.2
    ax.text(x_var, header_y, "变量", ha="left", va="bottom", fontsize=12, fontweight="bold")
    ax.text(x_or, header_y, "OR(95% CI)", ha="center", va="bottom", fontsize=12, fontweight="bold")
    if p_vals is not None:
        ax.text(x_pval, header_y, "P Value", ha="right", va="bottom", fontsize=12, fontweight="bold")

    # 三线表横线 + OR=ref 参考虚线
    line_top, line_mid, line_bot = header_y + 0.5, header_y - 0.2, -0.8
    for ly in (line_top, line_mid, line_bot):
        ax.plot([x_var, x_pval], [ly, ly], color="black", lw=1.5)
    ax.plot([ref, ref], [line_bot, line_top], color="black", ls="--", lw=1.5, zorder=1)

    # 手动 X 轴刻度
    if x_ticks is None:
        x_ticks = np.linspace(ors.min() * 0.8, ors.max() * 1.2, 4)
    for t in x_ticks:
        ax.plot([t, t], [line_bot, line_bot - 0.15], color="black", lw=1.5)
        ax.text(t, line_bot - 0.3, f"{t:.1f}", ha="center", va="top", fontsize=10)

    ax.axis("off")
    ax.set_xlim(x_var - 0.1, x_pval + 0.1)
    ax.set_ylim(line_bot - 0.8, line_top + 0.5)
    if title:
        ax.set_title(title, pad=20)


if __name__ == "__main__":
    use_theme("journal")

    # ① 数据区（替换成你的回归结果）
    labels = ["性别观念指数 (G)", "经济成本感知 (C)", "ln(个人年收入)", "年龄",
              "女性 (vs 男性)", "已婚/同居", "城镇居住"]
    ors = [1.095, 1.018, 0.896, 1.013, 0.793, 1.519, 0.919]
    ci_low = [1.036, 0.977, 0.842, 1.006, 0.693, 1.300, 0.836]
    ci_high = [1.158, 1.061, 0.953, 1.020, 0.908, 1.775, 1.010]
    p_vals = ["<0.001", "0.389", "<0.001", "<0.001", "0.001", "<0.001", "0.079"]

    # ② 图形设置区
    fig, ax = plt.subplots(figsize=(10, 5))
    forest_plot(ax, labels, ors, ci_low, ci_high, p_vals,
                x_ticks=[0.5, 1.0, 1.5, 2.0],
                title="图4 生育意愿影响因素的 Logit 回归森林图")
    save_fig(fig, "图4_森林图")
    plt.show()
