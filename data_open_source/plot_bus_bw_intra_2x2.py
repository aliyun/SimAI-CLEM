import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams["font.weight"] = 'medium'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['ytick.labelsize'] = 36  # 全局设置 Y 轴刻度字体大小
plt.rcParams['xtick.labelsize'] = 36  # 全局设置 X 轴刻度字体大小

H100_marker = "s"
A100_marker = "o"
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



def plot_subfigure(title: str, data_A100: dict, data_H100: dict, ax: plt.Axes, set_x_label: bool, set_y_label: bool):
    x = range(len(data_A100["NCCL_result"]))
    ax.plot(x, data_A100["Verse_result"], marker=A100_marker, color=Verse_color, linewidth=4, ms=15, ls=Verse_ls, alpha=0.85)
    ax.plot(x, data_A100['Astra_result'], marker=A100_marker, color=Astra_color, linewidth=4, ms=15, ls=Astra_ls, alpha=0.85)
    ax.plot(x, data_A100["NCCL_result"], marker=A100_marker, color=NCCL_color, linewidth=4, ms=15, ls=NCCL_ls, alpha=0.85)
    ax.plot(x, data_A100["SimAI_result"], marker=A100_marker, color=SimAI_color, linewidth=4, ms=15, ls=SimAI_ls, alpha=0.85)
    ax.plot(x, data_A100["CLEM_result"], marker=A100_marker, color=CLEM_color, linewidth=4, ms=15, ls=CLEM_ls, alpha=0.85)

    ax.plot(x, data_H100["Verse_result"], marker=H100_marker, color=Verse_color, linewidth=4, ms=15, ls=Verse_ls, alpha=0.85)
    ax.plot(x, data_H100["Astra_result"], marker=H100_marker, color=Astra_color, linewidth=4, ms=15, ls=Astra_ls, alpha=0.85)
    ax.plot(x, data_H100["NCCL_result"], marker=H100_marker, color=NCCL_color, linewidth=4, ms=15, ls=NCCL_ls, alpha=0.85)
    ax.plot(x, data_H100["SimAI_result"], marker=H100_marker, color=SimAI_color, linewidth=4, ms=15, ls=SimAI_ls, alpha=0.85)
    ax.plot(x, data_H100["CLEM_result"], marker=H100_marker, color=CLEM_color, linewidth=4, ms=15, ls=CLEM_ls, alpha=0.85)
    
    
    # 16M - 8G
    ax.set_ylim(bottom=0)
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
        "ReduceScatter A100": {
            "NCCL_result": [100.801, 136.915, 162.752, 183.698, 198.393, 209.555, 219.075, 222.648, 225.049, 226.918],
            "SimAI_result": [104.08419, 142.720123, 175.225418, 197.432785, 210.990616, 218.494141, 222.448883, 224.477371, 225.506409, 226.01796],
            "CLEM_result": [98.9556, 135.644, 178.197, 206.298, 214.43, 215.448, 218.016, 220.982, 220.094, 221.074],
            "Verse_result": [74.06639236989477, 111.75588236778468, 149.89330139851225, 180.7311372576135, 201.45388385665404, 213.70569923036334, 220.4079720502173, 223.91926826491436, 225.71720680240225, 226.627046997467],
            "Astra_result": [153.40791907454044, 170.5110547, 181.3579425599402, 186.89855736713534, 190.0084406481033, 191.60032971949778, 192.35447840720244, 192.73378341688849, 192.9373091500816, 193.0325701748238]
        },
        "ReduceScatter H100": {
            "NCCL_result": [210.72, 261.63, 290.36, 312.33, 328.77, 338.01, 345.39, 351.39, 356.33, 363.5],
            "SimAI_result": [223.626862, 273.014343, 306.552856, 326.228638, 337.356934, 343.20697, 346.20874, 347.730347, 348.489899, 348.862366],
            "CLEM_result": [217.4, 265.34, 297.77, 330.26, 338.69, 338.133, 346.81, 347.42, 346.443, 347.532],
            "Verse_result": [119.24219544867336, 179.56060276407413, 240.35116085812675, 289.3272929879867, 322.14932711968896, 341.52082882749477, 352.1072968535402, 357.65052515687756, 360.4881089078696, 361.9238529821557],
            "Astra_result": [248.82729630320188, 279.9909213148835, 299.7200651296212, 310.11407944526155, 315.5743258403568, 318.5222627620918, 319.9467992689259, 320.69910133166076, 321.0589157047178, 321.24681461563716]
        },
        "AllGather A100": {
            "NCCL_result": [93.9284, 129.62, 161.613, 177.249, 194.419, 205.807, 217.446, 222.011, 225.387, 226.916],
            "SimAI_result": [104.22702, 142.85434, 175.326523, 197.496964, 211.027252, 218.513794, 222.459061, 224.482544, 225.509033, 226.019302],
            "CLEM_result": [89.4444, 133.942, 173.844, 204.556, 209.169, 211.657, 217.441, 220.057, 219.703, 222.023],
            "Verse_result": [67.17961800051282, 103.75427582253994, 142.56179748342117, 175.3563218818213, 198.1469070625615, 211.91811837791084, 219.54739091840102, 223.57179950567163, 225.63984257438716, 226.6882778484245],
            "Astra_result": [154.76647022234403, 171.34694687450758, 181.82967167377322, 187.14873829727898, 190.13764357604217, 191.66599603988834, 192.3875648945827, 192.75039054289692, 192.94562990126707, 193.03673456997123]
        },
        "AllGather H100": {
            "NCCL_result": [218.69, 253.91, 293.22, 310.35, 327.82, 339.16, 347.92, 356, 359.9, 363.31],
            "SimAI_result": [224.287186, 273.50589, 306.862518, 326.40387, 337.450623, 343.255432, 346.233398, 347.742798, 348.496155, 348.865509],
            "CLEM_result": [230.55, 274.2, 299.29, 331.917, 334.839, 336.868, 343.224, 346.333, 351.636, 349.852],
            "Verse_result": [133.55061281417028, 195.38328003188172, 254.2382231739712, 299.3200323261379, 328.4396800078748, 345.2328405014107, 354.29029323591266, 358.9996105763154, 361.4015314465495, 362.6145850460718],
            "Astra_result": [252.42127344945578, 282.2519298987704, 301.0106573301825, 310.8034753520474, 315.9308796608277, 318.70378438740903, 320.0383477520054, 320.74508452414784, 321.08195727156374, 321.2583485]
        },
        "AllReduce A100": {
            "NCCL_result": [115.893, 140.563, 182.079, 196.281, 212.425, 221.603, 228.638, 231.543, 231.635, 231.585],
            "SimAI_result": [124.10981, 160.48262, 188.011292, 205.281296, 215.391617, 220.830841, 223.654175, 225.08963, 225.815231, 226.172729],
            "CLEM_result": [102.38, 149.501, 185.121, 216.246, 222.005, 225.285, 227.952, 226.05, 227.108, 227.238],
            "Verse_result": [107.4421300282607, 146.925147417855, 179.99816367626087, 202.82638792273582, 216.55890361431196, 224.14692302638903, 228.14389633302588, 230.19631920532518, 231.23644118189134, 231.76003492667652],
            "Astra_result": [155.722776, 171.931427, 182.158237, 187.32262, 190.227343, 191.711559, 192.4105155, 192.7619085, 193.07035, 193.099135]
        },
        "AllReduce H100": {
            "NCCL_result": [233.71, 273.435, 324.855, 332.755, 347.185, 355.215, 360.425, 363.865, 366.585, 368.095],
            "SimAI_result": [253.436295, 294.165894, 319.455933, 333.368378, 341.134583, 345.15213, 347.196594, 348.228668, 348.740326, 348.987396],
            "CLEM_result": [227.47, 280.66, 313.2, 341.33, 342.85, 345.13, 351.06, 353.74, 352.67, 351.95],
            "Verse_result": [185.69429625281782, 246.94971125980786, 295.7255538545331, 328.1306290214801, 347.1507044339955, 357.5122955517994, 362.9285560617969, 365.6986977320666, 367.09968716037275, 367.80421498625486],
            "Astra_result": [253.2158793952514, 282.7479980931928, 301.2925249301545, 310.9536603222053, 316.00845179001834, 318.74324948288245, 320.0582446779971, 320.7550766638743, 321.0869637635997, 321.2608544520276]
        },
        "AlltoAll A100": {
            "NCCL_result": [115.395, 152.31, 168.51, 183.32, 197.835, 206.04, 214.64, 215.06, 206.985, 213.63],
            "SimAI_result": [118.328186,155.486771,184.406189,203.310974,214.296906,220.247452,223.348404,224.931854,225.056522,225.132956],
            "CLEM_result": [115.27,147.22,174.96,195.73,206.35,213.60,218.62,219.11,220.09,220.29],
            "Verse_result": [102.5531,138.4591,167.8414,187.7641,199.6109,206.1132,209.5258,211.2749,212.1604,212.606],
            "Astra_result": [172.96,202.14,220.82,231.48,237.22,240.19,241.71,242.47,242.92,243.28]
        },
        "AlltoAll H100": {
            "NCCL_result": [204.135, 238.9, 279.295, 300.7, 314.335, 322.31, 334.455, 340.42, 342.97, 345.04],
            "SimAI_result": [212.583389,264.361969,300.930511,323.290527,335.76828,342.373535,345.775574,347.502075,347.872501,348.145742],
            "CLEM_result": [184.06,237.34,274.52,302.42,316.68,325.15,329.25,329.25,332.46,334.62],
            "Verse_result": [139.7118,198.9959,252.5859,291.8892,316.5145,330.454,337.8945,341.7419,343.6986,344.6854],
            "Astra_result": [263.89,309.79,339.30,356.27,365.39,370.13,372.55,373.24,374.47,374.96]
        }
    }
    fig, axes = plt.subplots(figsize=(20, 15), nrows=2, ncols=2, sharex=True, sharey=True)
    plot_subfigure("All Reduce", data["AllReduce A100"], data["AllReduce H100"], axes[0, 0], False, True)
    plot_subfigure("Reduce Scatter", data["ReduceScatter A100"], data["ReduceScatter H100"], axes[0,1], False, False)
    plot_subfigure("All Gather", data["AllGather A100"], data["AllGather H100"], axes[1,0], True, True)
    plot_subfigure("All to All", data["AlltoAll A100"], data["AlltoAll H100"], axes[1,1], True, False)

    
    NCCL_H100_line = Line2D([0], [0], color=NCCL_color, lw=2, marker=H100_marker, ms=15, ls=NCCL_ls, label="NCCL (H100)", alpha=0.85)
    NCCL_A100_line = Line2D([0], [0], color=NCCL_color, lw=2, marker=A100_marker, ms=15, ls=NCCL_ls, label="NCCL (A100)", alpha=0.85)
    CLEM_H100_line = Line2D([0], [0], color=CLEM_color, lw=2, marker=H100_marker, ms=15, ls=CLEM_ls, label="CLEM (H100)", alpha=0.85)
    CLEM_A100_line = Line2D([0], [0], color=CLEM_color, lw=2, marker=A100_marker, ms=15, ls=CLEM_ls, label="CLEM (A100)", alpha=0.85)
    SimAI_H100_line = Line2D([0], [0], color=SimAI_color, lw=2, marker=H100_marker, ms=15, ls=SimAI_ls, label="SimAI (H100)", alpha=0.85)
    SimAI_A100_line = Line2D([0], [0], color=SimAI_color, lw=2, marker=A100_marker, ms=15, ls=SimAI_ls, label="SimAI (A100)", alpha=0.85)
    Astra_H100_line = Line2D([0], [0], color=Astra_color, lw=2, marker=H100_marker, ms=15, ls=Astra_ls, label="AstraSim (H100)", alpha=0.85)
    Astra_A100_line = Line2D([0], [0], color=Astra_color, lw=2, marker=A100_marker, ms=15, ls=Astra_ls, label="AstraSim (A100)", alpha=0.85)
    Verse_H100_line = Line2D([0], [0], color=Verse_color, lw=2, marker=H100_marker, ms=15, ls=Verse_ls, label="Multiverse (H100)", alpha=0.85)
    Verse_A100_line = Line2D([0], [0], color=Verse_color, lw=2, marker=A100_marker, ms=15, ls=Verse_ls, label="Multiverse (A100)", alpha=0.85)

    fig.legend(handles=[NCCL_H100_line, NCCL_A100_line, CLEM_H100_line, CLEM_A100_line, SimAI_H100_line, SimAI_A100_line, Verse_H100_line, Verse_A100_line, Astra_H100_line, Astra_A100_line],loc="upper center", fontsize=23, ncol=5)
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.savefig("./bus_bw_intra_2x2.pdf", format='pdf',dpi=1000)
    plt.savefig("./bus_bw_intra_2x2.png", format='png')
    print(f"saving figure to ./bus_bw_intra_2x2.pdf and ./bus_bw_intra_2x2.png")
