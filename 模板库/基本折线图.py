# -*- coding: utf-8 -*-
"""
【提取自 学习笔记/基本折线图.md】学术简洁风时间序列折线图（多系列 + 对数坐标）
配套数据：data.csv（示例，可替换）；参考图：参考_折线图.png
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def create_chart(ax):
    df = pd.read_csv("data.csv")
    x = df["年份"].values
    cols = ["GDP总量", "第一产业", "第二产业", "第三产业"]
    y = df[cols].values
    colors = ["#b25f76", "#f6b014", "#7674b9", "#90abd4"]

    for i in range(4):
        ax.plot(x, y[:, i], label=cols[i], linewidth=3, color=colors[i])

    ax.set_yscale("log")  # 对数坐标
    ax.fill_betweenx([y.min(), y.max()], 2000, 2014, alpha=0.1, color=colors[0])
    ax.legend(loc="upper left", ncol=2)
    ax.set_xlabel("年份")
    ax.grid(axis="y", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    create_chart(ax)
    plt.tight_layout()
    plt.show()
