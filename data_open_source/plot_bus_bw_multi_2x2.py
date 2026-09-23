import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams["font.weight"] = 'medium'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['ytick.labelsize'] = 36  # 全局设置 Y 轴刻度字体大小
plt.rcParams['xtick.labelsize'] = 36  # 全局设置 X 轴刻度字体大小

multi_marker = "o"
NCCL_color = "firebrick"
CLEM_color = "#FE7743"
SimAI_color = "green"
Verse_color = "#0065F8" # Multiverse
Astra_color = "#BA487F" 

NCCL_ls = "-"
CLEM_ls = ":"
SimAI_ls = "--"
Astra_ls = "-."
Verse_ls = ":"



def plot_subfigure(title: str, data_set: dict, ax: plt.Axes,  set_x_label: bool, set_y_label: bool):
    x = range(len(data_set["NCCL_result"]))
    ax.plot(x, data_set["Verse_result"], marker=multi_marker, color=Verse_color, linewidth=4, ms=15, ls=Verse_ls, alpha=0.85)
    ax.plot(x, data_set['Astra_result'], marker=multi_marker, color=Astra_color, linewidth=4, ms=15, ls=Astra_ls, alpha=0.85)
    ax.plot(x, data_set["NCCL_result"], marker=multi_marker, color=NCCL_color, linewidth=4, ms=15, ls=NCCL_ls, alpha=0.85)
    ax.plot(x, data_set["SimAI_result"], marker=multi_marker, color=SimAI_color, linewidth=4, ms=15, ls=SimAI_ls, alpha=0.85)
    ax.plot(x, data_set["CLEM_result"], marker=multi_marker, color=CLEM_color, linewidth=4, ms=15, ls=CLEM_ls, alpha=0.85)
    
    # 16M - 8G
    ax.set_ylim(bottom=10, top=50)
    ax.set_yticks([10,20,30,40,50])
    ax.set_title(title, fontsize=40)
    ax.grid(True)
    ax.set_xticks([0,2,4,6,8])
    ax.set_xticklabels([16, 64, 256, 1024, 4096])
    if set_x_label:
        ax.set_xlabel("Data size (MiB)", fontsize=40)
    if set_y_label:
        ax.set_ylabel("Bus bw (GB/s)", fontsize=40)
    
if __name__=="__main__":
    data = {
        "MultiAllReduce 8 Nodes": {
            "NCCL_result": [36.865,41.61,42.34,42.84,43.015,43.095,43.155,43.17,43.27,43.355],
            "SimAI_result": [39.991905,43.122784,44.879543,45.812714,46.294006,46.538429,46.661594,46.723431,46.754414,46.76992],
            "CLEM_result": [39.97,43.33,43.49,43.63,43.63,43.67,43.66,43.71,43.74,43.72],
            "Verse_result": [38.43,42.70,45.21,46.53,47.24,47.59,47.78,47.87,47.92,47.94],
            "Astra_result": [39.97,43.63,45.72,46.80,47.38,47.67,47.81,47.89,47.93,47.95]
        },
        "MultiAllReduce 16 Nodes": {
            "NCCL_result": [29.44,38.35,43.35,43.605,43.78,43.865,43.915,43.965,43.69,44.16],
            "SimAI_result": [34.632137,39.658783,42.763508,44.505596,45.430965,45.908234,46.150616,46.272751,46.334072,46.342468],
            "CLEM_result": [31.72,40.17,44.29,44.21,44.27,44.30,44.31,44.29,44.33,44.32],
            "Verse_result": [29.96,35.92,39.88,42.21,43.43,44.10,44.42,44.60,44.84,44.89],
            "Astra_result": [31.94,37.30,40.72,42.68,43.68,44.22,44.49,44.63,44.70,44.73]
        },
        "MultiAllReduce 32 Nodes": {
            "NCCL_result": [21.95,30.045,39,43.915,44.06,44.205,44.24,44.255,44.305,44.4],
            "SimAI_result": [27.522196,34.500805,39.508343,42.601257,44.336712,45.258564,45.734016,45.975475,46.097141,46.204785],
            "CLEM_result": [22.96,32.91,40.57,44.67,44.60,44.62,44.63,44.64,44.63,44.67],
            "Verse_result": [22.13,29.03,34.78,38.61,40.86,42.04,42.68,42.99,43.04,43.11],
            "Astra_result": [24.40,30.91,36.10,39.41,41.30,42.27,42.80,43.05,43.17,43.22]
        },
        "MultiAllReduce 54 Nodes": {
            "NCCL_result": [13.86,26.81,36.355,44.34,45.935,46.545,48.2,48.695,48.695,48.805],
            "SimAI_result": [21.498262,29.328959,35.862122,40.357674,43.056377,44.54554,45.329323,45.731758,45.935612,46.183426],
            "CLEM_result":  [14.39,23.34,33.93,43.96,42.27,44.73,46.27,46.42,46.33,46.38],
            "Verse_result": [16.27,23.42,30.34,35.59,38.84,40.70,41.69,42.23,42.85,43.03],
            "Astra_result": [18.41,25.56,32.08,36.76,39.52,41.07,41.89,42.33,42.93,43.25]
        }
    }
    fig, axes = plt.subplots(figsize=(20, 15), nrows=2, ncols=2, sharex=True, sharey=True)
    plot_subfigure("8 Nodes", data["MultiAllReduce 8 Nodes"], axes[0, 0], False, True)
    plot_subfigure("16 Nodes", data["MultiAllReduce 16 Nodes"], axes[0,1], False, False)
    plot_subfigure("32 Nodes", data["MultiAllReduce 32 Nodes"], axes[1,0], True, True)
    plot_subfigure("54 Nodes", data["MultiAllReduce 54 Nodes"], axes[1,1], True, False)
    
    NCCL_multi_line = Line2D([0], [0], color=NCCL_color, lw=2, marker=multi_marker, ms=15, ls=NCCL_ls, label="NCCL", alpha=0.85)
    CLEM_multi_line = Line2D([0], [0], color=CLEM_color, lw=2, marker=multi_marker, ms=15, ls=CLEM_ls, label="CLEM", alpha=0.85)
    SimAI_multi_line = Line2D([0], [0], color=SimAI_color, lw=2, marker=multi_marker, ms=15, ls=SimAI_ls, label="SimAI", alpha=0.85)
    Astra_multi_line = Line2D([0], [0], color=Astra_color, lw=2, marker=multi_marker, ms=15, ls=Astra_ls, label="AstraSim", alpha=0.85)
    Verse_multi_line = Line2D([0], [0], color=Verse_color, lw=2, marker=multi_marker, ms=15, ls=Verse_ls, label="Multiverse", alpha=0.85)

    fig.legend(handles=[NCCL_multi_line, CLEM_multi_line, SimAI_multi_line, Verse_multi_line, Astra_multi_line],loc="upper center", fontsize=30, ncol=5)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.savefig("./bus_bw_multi_all_reduce_2x2.pdf", format='pdf',dpi=1000)
    plt.savefig("./bus_bw_multi_all_reduce_2x2.png", format='png')
    print(f"saving figure to ./bus_bw_multi_all_reduce_2x2.pdf and ./bus_bw_multi_all_reduce_2x2.png")
