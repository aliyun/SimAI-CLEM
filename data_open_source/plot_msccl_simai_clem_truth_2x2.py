import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


plt.rcParams["font.weight"] = 'medium'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']+plt.rcParams['font.serif']
plt.rcParams['ytick.labelsize'] = 22  # 全局设置 Y 轴刻度字体大小
plt.rcParams['xtick.labelsize'] = 22  # 全局设置 X 轴刻度字体大小

hatch_clem = '\\'
hatch_nccl = '..'
hatch_smai = 'x'

bar_lw = 2
deviation_font_size = 20
bar_width = 1.0

clem_qplb_color = clem_base_color = "#90C67C" # 浅绿
nccl_qplb_color = nccl_base_color = "#9EC6F3" # 浅蓝
smai_qplb_color = smai_base_color = "#C9B194" # 浅褐    

def plot_data_of_one_task_type(task_name: str, nccl_dataset: dict, clem_dataset: dict, smai_dataset: dict, ax: plt.Axes):
    # 64MB baseline
    ax[0][0].bar(x=0, height=clem_dataset['64MB']['native_nccl'], width=bar_width, bottom=0, color=clem_base_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (baseline)")
    ax[0][0].bar(x=1, height=nccl_dataset['64MB']['native_nccl'], width=bar_width, bottom=0, color=nccl_base_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (baseline)")
    ax[0][0].bar(x=2, height=smai_dataset['64MB']['native_nccl'], width=bar_width, bottom=0, color=smai_base_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (baseline)")
    # 64MB TECCL
    ax[0][0].bar(x=3.5, height=clem_dataset['64MB']['teccl'], width=bar_width, bottom=0, color=clem_qplb_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (QPLB)")
    ax[0][0].bar(x=4.5, height=nccl_dataset['64MB']['teccl'], width=bar_width, bottom=0, color=nccl_qplb_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (QPLB)")
    ax[0][0].bar(x=5.5, height=smai_dataset['64MB']['teccl'], width=bar_width, bottom=0, color=smai_qplb_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (QPLB)")
    # 64MB syccl
    ax[0][0].bar(x=7, height=clem_dataset['64MB']['syccl'], width=bar_width, bottom=0, color=clem_qplb_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (QPLB)")
    ax[0][0].bar(x=8, height=nccl_dataset['64MB']['syccl'], width=bar_width, bottom=0, color=nccl_qplb_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (QPLB)")
    ax[0][0].bar(x=9, height=smai_dataset['64MB']['syccl'], width=bar_width, bottom=0, color=smai_qplb_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (QPLB)")
    
    # 256MB baseline
    ax[0][1].bar(x=0, height=clem_dataset['256MB']['native_nccl'], width=bar_width, bottom=0, color=clem_base_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (baseline)")
    ax[0][1].bar(x=1, height=nccl_dataset['256MB']['native_nccl'], width=bar_width, bottom=0, color=nccl_base_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (baseline)")
    ax[0][1].bar(x=2, height=smai_dataset['256MB']['native_nccl'], width=bar_width, bottom=0, color=smai_base_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (baseline)")
    # 256MB TECCL
    ax[0][1].bar(x=3.5, height=clem_dataset['256MB']['teccl'], width=bar_width, bottom=0, color=clem_qplb_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (QPLB)")
    ax[0][1].bar(x=4.5, height=nccl_dataset['256MB']['teccl'], width=bar_width, bottom=0, color=nccl_qplb_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (QPLB)")
    ax[0][1].bar(x=5.5, height=smai_dataset['256MB']['teccl'], width=bar_width, bottom=0, color=smai_qplb_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (QPLB)")
    # 256MB syccl
    ax[0][1].bar(x=7, height=clem_dataset['256MB']['syccl'], width=bar_width, bottom=0, color=clem_qplb_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (QPLB)")
    ax[0][1].bar(x=8, height=nccl_dataset['256MB']['syccl'], width=bar_width, bottom=0, color=nccl_qplb_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (QPLB)")
    ax[0][1].bar(x=9, height=smai_dataset['256MB']['syccl'], width=bar_width, bottom=0, color=smai_qplb_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (QPLB)")
    
    # 1GB baseline
    ax[1][0].bar(x=0, height=clem_dataset['1GB']['native_nccl'], width=bar_width, bottom=0, color=clem_base_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (baseline)")
    ax[1][0].bar(x=1, height=nccl_dataset['1GB']['native_nccl'], width=bar_width, bottom=0, color=nccl_base_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (baseline)")
    ax[1][0].bar(x=2, height=smai_dataset['1GB']['native_nccl'], width=bar_width, bottom=0, color=smai_base_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (baseline)")
    # 1GB TECCL
    ax[1][0].bar(x=3.5, height=clem_dataset['1GB']['teccl'], width=bar_width, bottom=0, color=clem_qplb_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (QPLB)")
    ax[1][0].bar(x=4.5, height=nccl_dataset['1GB']['teccl'], width=bar_width, bottom=0, color=nccl_qplb_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (QPLB)")
    ax[1][0].bar(x=5.5, height=smai_dataset['1GB']['teccl'], width=bar_width, bottom=0, color=smai_qplb_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (QPLB)")
    # 1GB syccl
    ax[1][0].bar(x=7, height=clem_dataset['1GB']['syccl'], width=bar_width, bottom=0, color=clem_qplb_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (QPLB)")
    ax[1][0].bar(x=8, height=nccl_dataset['1GB']['syccl'], width=bar_width, bottom=0, color=nccl_qplb_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (QPLB)")
    ax[1][0].bar(x=9, height=smai_dataset['1GB']['syccl'], width=bar_width, bottom=0, color=smai_qplb_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (QPLB)")

    # 4GB baseline
    ax[1][1].bar(x=0, height=clem_dataset['4GB']['native_nccl'], width=bar_width, bottom=0, color=clem_base_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (baseline)")
    ax[1][1].bar(x=1, height=nccl_dataset['4GB']['native_nccl'], width=bar_width, bottom=0, color=nccl_base_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (baseline)")
    ax[1][1].bar(x=2, height=smai_dataset['4GB']['native_nccl'], width=bar_width, bottom=0, color=smai_base_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (baseline)")
    # 4GB TECCL
    ax[1][1].bar(x=3.5, height=clem_dataset['4GB']['teccl'], width=bar_width, bottom=0, color=clem_qplb_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (QPLB)")
    ax[1][1].bar(x=4.5, height=nccl_dataset['4GB']['teccl'], width=bar_width, bottom=0, color=nccl_qplb_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (QPLB)")
    ax[1][1].bar(x=5.5, height=smai_dataset['4GB']['teccl'], width=bar_width, bottom=0, color=smai_qplb_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (QPLB)")
    # 4GB syccl
    ax[1][1].bar(x=7, height=clem_dataset['4GB']['syccl'], width=bar_width, bottom=0, color=clem_qplb_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM (QPLB)")
    ax[1][1].bar(x=8, height=nccl_dataset['4GB']['syccl'], width=bar_width, bottom=0, color=nccl_qplb_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="NCCL (QPLB)")
    ax[1][1].bar(x=9, height=smai_dataset['4GB']['syccl'], width=bar_width, bottom=0, color=smai_qplb_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI (QPLB)")


    ax[0][0].set_xticks([1, 4.5, 8])
    ax[0][0].set_xticklabels(["Ring", "TECCL", "SyCCL"], fontsize=22)
    ax[0][1].set_xticks([1, 4.5, 8])
    ax[0][1].set_xticklabels(["Ring", "TECCL", "SyCCL"], fontsize=22)
    ax[1][0].set_xticks([1, 4.5, 8])
    ax[1][0].set_xticklabels(["Ring", "TECCL", "SyCCL"], fontsize=22)
    ax[1][1].set_xticks([1, 4.5, 8])
    ax[1][1].set_xticklabels(["Ring", "TECCL", "SyCCL"], fontsize=22)
    
    ax[0][0].set_ylabel("Bus bw (GB/s)", fontsize=24)
    ax[1][0].set_ylabel("Bus bw (GB/s)", fontsize=24)
    ax[0][0].set_yticks([0,20,40,60,80,100,120])
    ax[1][0].set_yticks([0,20,40,60,80,100,120])
    
    ax[0][0].set_xlabel("64MB", fontsize=24)
    ax[0][1].set_xlabel("256MB",  fontsize=24)
    ax[1][0].set_xlabel("1GB", fontsize=24)
    ax[1][1].set_xlabel("4GB",  fontsize=24)
    ax[0][0].grid(True, linestyle="--", alpha=0.6)
    ax[0][1].grid(True, linestyle="--", alpha=0.6)
    ax[1][0].grid(True, linestyle="--", alpha=0.6)
    ax[1][1].grid(True, linestyle="--", alpha=0.6)
    return

def calculate_precision(nccl_dataset: dict, clem_dataset: dict, smai_dataset: dict):
    for algo in ['native_nccl', 'teccl', 'syccl']:
        clem_dev_list = []
        smai_dev_list = []
        for msg_size in ['64MB', '256MB', '1GB', '4GB']:
            clem_dev = abs(clem_dataset[msg_size][algo] - nccl_dataset[msg_size][algo]) / nccl_dataset[msg_size][algo]
            smai_dev = abs(smai_dataset[msg_size][algo] - nccl_dataset[msg_size][algo]) / nccl_dataset[msg_size][algo]
            clem_dev_list.append(clem_dev)
            smai_dev_list.append(smai_dev)
            # print(f"{algo} {msg_size} precision: {clem_dev:.6f}, {smai_dev:.6f}")
        avg_clem_prec = 100 - sum(clem_dev_list) / len(clem_dev_list) * 100
        avg_smai_prec = 100 - sum(smai_dev_list) / len(smai_dev_list) * 100
        print(f"{algo} avg precision: {avg_clem_prec:.2f}%, {avg_smai_prec:.2f}%")
    return


# 示例数据
if __name__=="__main__":
    # 测试配置
    # 2 x A100 Global AllGather
    nccl_dataset = {
        '64MB': {'native_nccl': 75.9156, 'teccl': 79.0777, 'syccl': 80.5292},
        '256MB': {'native_nccl': 82.6604, 'teccl': 82.8142, 'syccl': 96.7068},
        '1GB': {'native_nccl': 90.8378, 'teccl': 95.9071, 'syccl': 113.83},
        '4GB': {'native_nccl': 94.0296, 'teccl': 106.365, 'syccl': 119.161}
    }
    
    clem_dataset = {
        '64MB': {'native_nccl': 75.7824, 'teccl': 77.6855, 'syccl': 73.2043},
        '256MB': {'native_nccl': 88.804, 'teccl': 77.6139, 'syccl': 101.817},
        '1GB': {'native_nccl': 92.0817, 'teccl': 89.8535, 'syccl': 111.435},
        '4GB': {'native_nccl': 92.629, 'teccl': 95.1587, 'syccl': 115.264}
    }

    smai_dataset = {
        '64MB': {'native_nccl': 74.768112, 'teccl': 34.836776, 'syccl': 105.0752641508},
        '256MB': {'native_nccl': 81.898788, 'teccl': 45.394398, 'syccl': 104.275623},
        '1GB': {'native_nccl': 83.640915, 'teccl': 49.679392, 'syccl': 109.421704831},
        '4GB': {'native_nccl': 84.339676, 'teccl': 52.536224, 'syccl': 107.462146277}
    }
    
    calculate_precision(nccl_dataset, clem_dataset, smai_dataset)
    
    fig, axs = plt.subplots(figsize=(13, 10), nrows=2, ncols=2, sharex=False, sharey=True)
    plot_data_of_one_task_type("no sense", nccl_dataset, clem_dataset, smai_dataset, axs)
    

    # 创建自定义矩形对象
    rect_nccl_base = Rectangle((0, 0), 2, 2, facecolor=nccl_base_color, hatch=hatch_nccl, edgecolor="black", linewidth=bar_lw , label="Ground Truth")
    rect_clem_base = Rectangle((0, 0), 2, 2, facecolor=clem_base_color, hatch=hatch_clem, edgecolor="black", linewidth=bar_lw , label="CLEM")
    rect_smai_base = Rectangle((0, 0), 2, 2, facecolor=smai_base_color, hatch=hatch_smai, edgecolor="black", linewidth=bar_lw , label="SimAI")

    # 添加自定义图例
    fig.legend(handles=[rect_nccl_base, rect_clem_base, rect_smai_base], loc="upper center", fontsize=22, ncol=3)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    fig_name = "plot_1x2_0529.png"
    plt.savefig(fig_name)
    plt.savefig("msccl_simai_clem_groundtruth_2x2.pdf", format="pdf", dpi=1000)
    print("saving figure to", fig_name)
    print("saving figure to msccl_simai_clem_groundtruth_2x2.pdf")
    
    print(plt.rcParams['font.family'])
