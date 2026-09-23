import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


plt.rcParams["font.weight"] = 'medium'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']+plt.rcParams['font.serif']
plt.rcParams['ytick.labelsize'] = 22  # 全局设置 Y 轴刻度字体大小
plt.rcParams['xtick.labelsize'] = 22  # 全局设置 X 轴刻度字体大小



bar_lw = 2
deviation_font_size = 20
bar_width = 1.0
hatch_clem = '\\'
hatch_nccl = '..'
hatch_smai = 'x'
clem_qplb_color = clem_base_color = "#90C67C" # 浅绿
nccl_qplb_color = nccl_base_color = "#9EC6F3" # 浅蓝
smai_qplb_color = smai_base_color = "#C9B194" # 浅褐
# smai_c4_p_color = "#884909" # 棕褐

def plot_data_of_one_task_type(task_name: str, nccl_dataset: dict, clem_dataset: dict, smai_dataset: dict, ax: plt.Axes, set_x_label: bool):
    # 1x128 baseline
    ax[0].bar(x=0, height=clem_dataset['1x128']['no_qplb'], width=bar_width, bottom=0, color=clem_base_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (baseline)")
    ax[0].bar(x=1, height=nccl_dataset['1x128']['no_qplb'], width=bar_width, bottom=0, color=nccl_base_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (baseline)")
    ax[0].bar(x=2, height=smai_dataset['1x128']['no_qplb'], width=bar_width, bottom=0, color=smai_base_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (baseline)")
    clem_deviation = abs(clem_dataset['1x128']['no_qplb'] - nccl_dataset['1x128']['no_qplb']) / nccl_dataset['1x128']['no_qplb']
    smai_deviation = abs(smai_dataset['1x128']['no_qplb'] - nccl_dataset['1x128']['no_qplb']) / nccl_dataset['1x128']['no_qplb']
    # ax[0].text(x=0, y=clem_dataset['1x128']['no_qplb'], s=f"{clem_deviation*100:.1f}%", ha='center', va='bottom', fontsize=deviation_font_size)
    # ax[0].text(x=2, y=smai_dataset['1x128']['no_qplb'], s=f"{smai_deviation*100:.1f}%", ha='center', va='bottom', fontsize=deviation_font_size)
    # 1x128 QPLB
    ax[0].bar(x=3.5, height=clem_dataset['1x128']['qplb_A'], width=bar_width, bottom=0, color=clem_qplb_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (QPLB)")
    ax[0].bar(x=4.5, height=nccl_dataset['1x128']['qplb_A'], width=bar_width, bottom=0, color=nccl_qplb_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (QPLB)")
    ax[0].bar(x=5.5, height=smai_dataset['1x128']['qplb_A'], width=bar_width, bottom=0, color=smai_qplb_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (QPLB)")
    clem_deviation = abs(clem_dataset['1x128']['qplb_A'] - nccl_dataset['1x128']['qplb_A']) / nccl_dataset['1x128']['qplb_A']
    smai_deviation = abs(smai_dataset['1x128']['qplb_A'] - nccl_dataset['1x128']['qplb_A']) / nccl_dataset['1x128']['qplb_A']
    # ax[0].text(x=3.5, y=clem_dataset['1x128']['qplb_A'], s=f"{clem_deviation*100:.1f}%", ha='center', va='bottom', fontsize=deviation_font_size)
    # ax[0].text(x=5.5, y=smai_dataset['1x128']['qplb_A'], s=f"{smai_deviation*100:.1f}%", ha='center', va='bottom', fontsize=deviation_font_size)
    # 1x128 C4P
    ax[0].bar(x=7, height=clem_dataset['1x128']['C4P'], width=bar_width, bottom=0, color=clem_qplb_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (QPLB)")
    ax[0].bar(x=8, height=nccl_dataset['1x128']['C4P'], width=bar_width, bottom=0, color=nccl_qplb_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (QPLB)")
    ax[0].bar(x=9, height=smai_dataset['1x128']['C4P'], width=bar_width, bottom=0, color=smai_qplb_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (QPLB)")
    clem_deviation = abs(clem_dataset['1x128']['C4P'] - nccl_dataset['1x128']['C4P']) / nccl_dataset['1x128']['C4P']
    smai_deviation = abs(smai_dataset['1x128']['C4P'] - nccl_dataset['1x128']['C4P']) / nccl_dataset['1x128']['C4P']
    # ax[0].text(x=7, y=clem_dataset['1x128']['C4P'], s=f"{clem_deviation*100:.1f}%", ha='center', va='bottom', fontsize=deviation_font_size)
    # ax[0].text(x=9, y=smai_dataset['1x128']['C4P'], s=f"{smai_deviation*100:.1f}%", ha='center', va='bottom', fontsize=deviation_font_size)
    
    # 4x32 baseline
    ax[1].bar(x=0, height=clem_dataset['4x32']['no_qplb'], width=bar_width, bottom=0, color=clem_base_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (baseline)")
    ax[1].bar(x=1, height=nccl_dataset['4x32']['no_qplb'], width=bar_width, bottom=0, color=nccl_base_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (baseline)")
    ax[1].bar(x=2, height=smai_dataset['4x32']['no_qplb'], width=bar_width, bottom=0, color=smai_base_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (baseline)")
    clem_deviation = abs(clem_dataset['4x32']['no_qplb'] - nccl_dataset['4x32']['no_qplb']) / nccl_dataset['4x32']['no_qplb']
    smai_deviation = abs(smai_dataset['4x32']['no_qplb'] - nccl_dataset['4x32']['no_qplb']) / nccl_dataset['4x32']['no_qplb']
    # ax[1].text(x=0, y=clem_dataset['4x32']['no_qplb'], s=f"{clem_deviation*100:.1f}%", ha='center', va='bottom', fontsize=deviation_font_size)
    # ax[1].text(x=2, y=smai_dataset['4x32']['no_qplb'], s=f"{smai_deviation*100:.1f}%", ha='center', va='bottom', fontsize=deviation_font_size)
    # 4x32 QPLB
    ax[1].bar(x=3.5, height=clem_dataset['4x32']['qplb_A'], width=bar_width, bottom=0, color=clem_qplb_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (QPLB)")
    ax[1].bar(x=4.5, height=nccl_dataset['4x32']['qplb_A'], width=bar_width, bottom=0, color=nccl_qplb_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (QPLB)")
    ax[1].bar(x=5.5, height=smai_dataset['4x32']['qplb_A'], width=bar_width, bottom=0, color=smai_qplb_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (QPLB)")
    clem_deviation = abs(clem_dataset['4x32']['qplb_A'] - nccl_dataset['4x32']['qplb_A']) / nccl_dataset['4x32']['qplb_A']
    smai_deviation = abs(smai_dataset['4x32']['qplb_A'] - nccl_dataset['4x32']['qplb_A']) / nccl_dataset['4x32']['qplb_A']
    # ax[1].text(x=3.5, y=clem_dataset['4x32']['qplb_A'], s=f"{clem_deviation*100:.1f}%", ha='center', va='bottom', fontsize=deviation_font_size)
    # ax[1].text(x=5.5, y=smai_dataset['4x32']['qplb_A'], s=f"{smai_deviation*100:.1f}%", ha='center', va='bottom', fontsize=deviation_font_size)
    # 4x32 C4P
    ax[1].bar(x=7, height=clem_dataset['4x32']['C4P'], width=bar_width, bottom=0, color=clem_qplb_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (QPLB)")
    ax[1].bar(x=8, height=nccl_dataset['4x32']['C4P'], width=bar_width, bottom=0, color=nccl_qplb_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (QPLB)")
    ax[1].bar(x=9, height=smai_dataset['4x32']['C4P'], width=bar_width, bottom=0, color=smai_qplb_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (QPLB)")
    clem_deviation = abs(clem_dataset['4x32']['C4P'] - nccl_dataset['4x32']['C4P']) / nccl_dataset['4x32']['C4P']
    smai_deviation = abs(smai_dataset['4x32']['C4P'] - nccl_dataset['4x32']['C4P']) / nccl_dataset['4x32']['C4P']
    # ax[1].text(x=7, y=clem_dataset['4x32']['C4P'], s=f"{clem_deviation*100:.1f}%", ha='center', va='bottom', fontsize=deviation_font_size)
    # ax[1].text(x=9, y=smai_dataset['4x32']['C4P'], s=f"{smai_deviation*100:.1f}%", ha='center', va='bottom', fontsize=deviation_font_size)
    ax[0].set_xticks([1, 4.5, 8])
    ax[0].set_xticklabels(["naive NCCL", "QPLB", "C4P"], fontsize=22)
    ax[1].set_xticks([1, 4.5, 8])
    ax[1].set_xticklabels(["naive NCCL", "QPLB", "C4P"], fontsize=22)
    ax[0].set_ylabel("Avg bus bw (GB/s)", fontsize=24)
    # ax[1].set_ylabel("Avg bus bw (GB/s)", fontsize=20)
    ax[0].set_xlabel("1x128", fontsize=24)
    ax[1].set_xlabel("4x32",  fontsize=24)
    ax[0].grid(True, linestyle="--", alpha=0.6)
    ax[1].grid(True, linestyle="--", alpha=0.6)
    return

def calculate_precision(nccl_dataset: dict, clem_dataset: dict, smai_dataset: dict):
    for strategy in ['no_qplb', 'qplb_A', 'C4P']:
        clem_precision_list = []
        smai_precision_list = []
        for workload in ['1x128', '4x32']:
            clem_precision = abs(clem_dataset[workload][strategy] - nccl_dataset[workload][strategy]) / nccl_dataset[workload][strategy]
            smai_precision = abs(smai_dataset[workload][strategy] - nccl_dataset[workload][strategy]) / nccl_dataset[workload][strategy]
            clem_precision_list.append(clem_precision)
            smai_precision_list.append(smai_precision)
        avg_clem_precision = 100 - sum(clem_precision_list) / len(clem_precision_list) * 100
        avg_smai_precision = 100 - sum(smai_precision_list) / len(smai_precision_list) * 100
        print(f"{strategy} avg precision: {avg_clem_precision:.1f}%, {avg_smai_precision:.1f}%")

# 示例数据
if __name__=="__main__":
    nccl_dataset = {
        '1x128': {'no_qplb': 51, 'qplb_A': 64, 'C4P': 83},
        '4x32': {'no_qplb': 49.75, 'qplb_A': 59.75, 'C4P': 79.75},
    }
    clem_dataset = {
        '1x128': {'no_qplb': 53.87423, 'qplb_A': 63.1947, 'C4P': 88.74},
        '4x32': {'no_qplb': 51.754675, 'qplb_A': 62.1046, 'C4P': 87.45},
    }
    smai_dataset = {
        '1x128': {'no_qplb': 46.599579, 'qplb_A': 48.610352, 'C4P': 61.208080},
        '4x32': {'no_qplb': 42.752789, 'qplb_A': 42.247871, 'C4P': 59.881893},
    }
    calculate_precision(nccl_dataset, clem_dataset, smai_dataset)
    
    fig, axs = plt.subplots(figsize=(12, 5), nrows=1, ncols=2, sharey=True)
    plot_data_of_one_task_type("no sense", nccl_dataset, clem_dataset, smai_dataset, axs, set_x_label=True)
    

    # 创建自定义矩形对象
    rect_nccl_base = Rectangle((0, 0), 1.6, 1.6, facecolor=nccl_base_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="Ground Truth")
    rect_clem_base = Rectangle((0, 0), 1.6, 1.6, facecolor=clem_base_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM")
    rect_smai_base = Rectangle((0, 0), 1.6, 1.6, facecolor=smai_base_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI")

    # 添加自定义图例
    fig.legend(handles=[rect_nccl_base, rect_clem_base, rect_smai_base], loc="upper center", fontsize=22, ncol=3)
    plt.tight_layout(rect=[0, 0, 1, 0.88])
    fig_name = "plot_1x2_0514.png"
    plt.savefig(fig_name)
    plt.savefig("simai_clem_nccl_C4P_vs_QPLB_vs_Baseline_v2.pdf", format="pdf", dpi=1000)
    print("saving figure to", fig_name)
    print("saving figure to simai_clem_nccl_C4P_vs_QPLB_vs_Baseline_v2.pdf")
    
    print(plt.rcParams['font.family'])
