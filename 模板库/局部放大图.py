# -*- coding: utf-8 -*-
"""
【提取自 学习笔记/局部放大图.md】TFR 对意愿调整速度 α 的敏感性分析
样条平滑 + 局部放大 inset + 参数区间阴影（紫色渐变专属色系）
参考图：参考_灵敏度分析图.png
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import make_interp_spline
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

# ===================== 1. 全局配置与配色 =====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Times New Roman']
plt.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['pdf.fonttype'] = 42

# 敏感性分析专有色系：紫色渐变（固定保留）
SENS_COLORS = {
    0.10: '#d9b3ff',  # 浅紫 (保守)
    0.20: '#a23b72',  # 中紫 (基准)
    0.30: '#4b0082'   # 深紫 (乐观)
}
COLOR_S0 = '#474747'  # S0 基准线 (深灰)

# 简易模拟类，保证代码独立可运行
class SDModel:
    """简易模拟类，仅供代码跑通"""
    def __init__(self, scenario='S1', alpha=0.2, **kwargs):
        self.years = np.arange(2025, 2036)
        self.scenario = scenario
        self.alpha = alpha

    def run(self):
        t = self.years - 2024.5
        if self.scenario == 'S0':
            self.TFR = 0.5 + 0.05 * np.sin(t / 5)
        else:
            growth = (self.alpha * 0.5) * (1 - np.exp(-0.4 * t))
            self.TFR = 0.55 + growth

# ===================== 2. 辅助工具函数 =====================
def get_smooth(x, y):
    """三次样条插值平滑曲线"""
    x_new = np.linspace(x.min(), x.max(), 300)
    spl = make_interp_spline(x, y, k=3)
    return x_new, spl(x_new)

# ===================== 3. 图(a) 独立绘图函数 =====================
def plot_tfr_sensitivity_only():
    """单独绘制：TFR 对意愿调整速度 α 的敏感性分析（含局部放大）"""
    alpha_list = [0.10, 0.20, 0.30]

    # 运行仿真模型
    m_S0 = SDModel(scenario='S0')
    m_S0.run()
    years = m_S0.years

    results = {}
    for a in alpha_list:
        m = SDModel(scenario='S1', alpha=a)
        m.run()
        results[a] = m

    # 创建单个画布（仅图a）
    fig, ax1 = plt.subplots(figsize=(10, 7))

    # 数据平滑处理
    y_s, tfr_s0 = get_smooth(years, m_S0.TFR)
    tfr_data = {a: get_smooth(years, results[a].TFR)[1] for a in alpha_list}

    # ==========================
    # 绘制 TFR 敏感性主图
    # ==========================
    # 填充参数区间阴影
    ax1.fill_between(y_s, tfr_data[0.10], tfr_data[0.30], color=SENS_COLORS[0.20], alpha=0.1)

    # 绘制基准线与参数曲线
    ax1.plot(y_s, tfr_s0, color=COLOR_S0, lw=1.5, ls='--', label='S0 基准', alpha=0.6)
    for a in alpha_list:
        lw = 3 if a == 0.20 else 1.5
        ax1.plot(y_s, tfr_data[a], color=SENS_COLORS[a], lw=lw, label=f'α={a:.2f}')

    # ==========================
    # 局部放大子图
    # ==========================
    ax_ins = inset_axes(ax1, width="35%", height="30%", loc='lower right',
                        bbox_to_anchor=(-0.09, 0.5, 1, 1), bbox_transform=ax1.transAxes)

    # 子图绘制曲线与填充
    ax_ins.fill_between(y_s, tfr_data[0.10], tfr_data[0.30], color=SENS_COLORS[0.20], alpha=0.1)
    ax_ins.plot(y_s, tfr_s0, color=COLOR_S0, lw=1, ls='--')
    for a in alpha_list:
        ax_ins.plot(y_s, tfr_data[a], color=SENS_COLORS[a], lw=(2 if a == 0.20 else 1))

    # 放大区域范围设置
    x1, x2, y1, y2 = 2033.3, 2034.7, min(tfr_data[0.10][-50:]), max(tfr_data[0.30][-1:]) + 0.02
    ax_ins.set_xlim(x1, x2)
    ax_ins.set_ylim(y1, y2)
    ax_ins.tick_params(labelsize=8)
    ax_ins.grid(True, alpha=0.2, ls='--')

    # 放大区域连接线
    mark_inset(ax1, ax_ins, loc1=3, loc2=4, fc="none", ec="gray", lw=0.8, ls="--", alpha=0.5)

    # ==========================
    # 图表样式美化
    # ==========================
    ax1.set_title('(a) TFR 对意愿调整速度 α 的敏感性', fontsize=13, fontweight='bold', pad=15)
    ax1.set_xlabel('年份', fontweight='bold')
    ax1.set_ylabel('总和生育率 TFR', fontweight='bold')
    ax1.set_xlim(2025, 2035)
    ax1.grid(True, alpha=0.15, ls='--')
    ax1.tick_params(direction='in', top=True, right=True)
    ax1.legend(loc='lower left', frameon=False, fontsize=9)

    # 画布比例优化
    yr = ax1.get_ylim()[1] - ax1.get_ylim()[0]
    xr = ax1.get_xlim()[1] - ax1.get_xlim()[0]
    ax1.set_aspect(xr / yr * 0.65)

    # 保存与显示
    plt.tight_layout()
    plt.savefig('局部放大图.png', dpi=300, bbox_inches='tight')
    plt.show()

# ===================== 执行 =====================
if __name__ == '__main__':
    plot_tfr_sensitivity_only()
