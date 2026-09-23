import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import re
import sys
from collections import defaultdict
from matplotlib.lines import Line2D

NUM_GPUS_PER_SERVER = 8
LINE_WIDTH = 3
FIG_STYLE = 'step'
# FIG_STYLE = 'plot'


plt.rcParams["font.weight"] = 'medium'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['ytick.labelsize'] = 34  # 全局设置 Y 轴刻度字体大小
plt.rcParams['xtick.labelsize'] = 34  # 全局设置 X 轴刻度字体大小

def get_nic_events_from_nccltest_log(nccltest_log, num_events_per_iter):
    """
    输入: nccltests的日志 这个日志只记录了rank 0的qp的postsend和pollcq的信息
    输出: 以PostSend Event和PollCq Event组成的列表
    """
    post_send_event_dict = {}
    poll_cq_event_dict = {}
    post_send_opcode_set = set()
    poll_cq_opcode_set = set()

    with open(nccltest_log, 'r') as file:
        for line in file:
            line = line.strip()
            if "PostSend" not in line and "PollCq" not in line:
                continue
            if not line:
                continue  # 跳过空行

            parts = line.split()
            if len(parts) != 5:
                continue  # 忽略不符合格式的行

            action, time_str, qp_num_str, opcode_str, wr_id_str = parts

            try:
                time = int(time_str)
                qp_num = int(qp_num_str)
                opcode = int(opcode_str)
                wr_id = int(wr_id_str)
            except ValueError:
                continue  # 如果转换失败，跳过该行

            if action == "PostSend":
                if qp_num not in post_send_event_dict:
                    post_send_event_dict[qp_num] = []
                post_send_event_dict[qp_num].append((action, time, opcode, wr_id))
                post_send_opcode_set.add(opcode)

            elif action == "PollCq":
                if qp_num not in poll_cq_event_dict:
                    poll_cq_event_dict[qp_num] = []
                poll_cq_event_dict[qp_num].append((action, time, opcode, wr_id))
                poll_cq_opcode_set.add(opcode)

    nic_events = []
    for qp_num in post_send_event_dict.keys():
        list1 = post_send_event_dict[qp_num]
        assert qp_num in poll_cq_event_dict
        list2 = poll_cq_event_dict[qp_num]
        nic_events.extend(list1)
        nic_events.extend(list2)
    print(f"len: {len(nic_events)}")
    # 因为nccl-tests有warmup 所以测一次AllReduce但是其实有好几次AllReduce
    nic_events.sort(key=lambda x: x[1])
    idx = -3
    nic_events = nic_events[idx*num_events_per_iter:(idx+1)*num_events_per_iter]
    # nic_events = nic_events[-num_events_per_iter:]

    return nic_events

def get_nic_events_from_clem_logs(ns3_log_file, clem_qp_logs_dir, src_idx_list, wr_size):
    node_pair_info = {}   # 按节点对统计 QpSendData 的 QP 数量和发送数据总量
    data_stat_pattern = r"QP\((\d+),(\d+)\) \(with remote_qp=QP\((\d+),(\d+)\)\): five_tuple (\S+) qp_use_propose (\S+) total_tx_bytes: (\d+)"
    # 读取日志文件
    with open(ns3_log_file, "r") as file:
        
        for line in file:
            # 匹配数据统计信息
            data_stat_match = re.search(data_stat_pattern, line)
            if data_stat_match:
                node1, qpnum1, node2, qpnum2, five_tuple, qp_type, tx_bytes = data_stat_match.groups()
                node1, qpnum1, node2, qpnum2, tx_bytes = map(int, [node1, qpnum1, node2, qpnum2, tx_bytes])
                qp1 = (node1, qpnum1)
                qp2 = (node2, qpnum2)
                # 如果类型为 QpSendData，则记录发送数据量
                if qp_type == "QpSendData" and node1 // NUM_GPUS_PER_SERVER != node2 // NUM_GPUS_PER_SERVER and node1 in src_idx_list:
                    # 按节点对统计
                    pair = (node1, node2)  # 确保节点对顺序一致
                    if pair not in node_pair_info:
                        node_pair_info[pair] = {"qps": [], "total_data_sent": 0}
                    node_pair_info[pair]["qps"].append(qp1)
                    node_pair_info[pair]["total_data_sent"] += tx_bytes 
    for pair, info in node_pair_info.items():
        print(f"Node pair: {pair}, NumQPs: {len(info['qps'])} QPs: {info['qps']}, Total data sent: {info['total_data_sent']}")
        # 因为其实整个dict只有一组值
        total_qps = info['qps']
    nic_events = []
    for qp in total_qps:
        qp_log_file = f"{clem_qp_logs_dir}QP({qp[0]},{qp[1]})_normal.log"
        qp_events = get_qp_events(qp_log_file, wr_size)
        nic_events.extend(qp_events)
    return nic_events

def get_qp_events(qp_file_path, wr_size):
    print(qp_file_path)
    """ 
    获取该QP日志文件所对应的nic_events
    """
    nic_events = []
    # 先读取文件 获取PostSend/WorkComplte时刻表
    pattern = re.compile(r'(\d+)\s+(EnqueueSendRequest|WriteWithImm\s+Complete|Write\s+Complete)\s+(\d+)\s+with\s+WrId\s*=\s*(\d+)')
    events = []
        # for msg in result:
        # if msg['src'] in src_idx_list:
        #     nic_events.append(('PostSend', msg['start_time'], 1, 0))
        #     nic_events.append(('PollCq', msg['end_time'], 1, 0))
    # 将每一行处理成一个Dict Entry
    with open(qp_file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                time, operation, size, wr_id = match.groups()
                if size != str(wr_size):
                    continue
                if "Complete" in operation:
                    # 说明是PollCq
                    nic_events.append(('PollCq', int(time), 1, 0))
                else:
                    # 说明是PostSend
                    nic_events.append(('PostSend', int(time), 1, 0))
    print(f"********** get_qp_events: {len(nic_events)} **********")
    return nic_events

def get_msg_intervals_from_events(event_list):
    msg_intervals = []
    # 按照时间先后顺序排序
    event_list.sort(key=lambda x: x[1])
    for i in range(len(event_list)):
        cur_event = event_list[i]
        if cur_event[0] == "PostSend":
            for next_event in event_list[i+1:]:
                if next_event[0] == "PollCq" and next_event[3] == cur_event[3]:
                    msg_intervals.append((cur_event[1], next_event[1], cur_event[2]))
                    break
    return msg_intervals

def get_num_inflight_vs_time(event_list, tag):
    """
    输入: 以PostSend Event和PollCq Event组成的列表
    输出: 每个时刻的num_inflight的列表
    """
    event_list.sort(key=lambda x: x[1])
    cur_num_inflight = 0
    tick_inflight = []
    for i in range(len(event_list)):
        cur_event = event_list[i]
        if cur_event[0] == 'PostSend':
            cur_num_inflight += 1
        elif cur_event[0] == 'PollCq':
            cur_num_inflight -= 1
        tick_inflight.append([cur_event[1], cur_num_inflight])
    if tag == 'nccl' or tag == 'simai':
        start_time = tick_inflight[0][0] - 10
    else:
        start_time = 0
    print(start_time)
    tick_inflight = [ [tick - start_time, num_inflight] for tick, num_inflight in tick_inflight]
    tick_inflight.insert(0, [0, 0])
    if tag == 'astra_sim':
        tick_inflight.append([5886394, 0])
        print("********",tick_inflight)
    return tick_inflight

def plot_num_inflight_N(tick_inflight_list_list, pattern_name_list, fig_name, fig_a, fig_b, y_tick_list):
    """
    输入: 每个时刻的num_inflight的列表
    输出: 图片
    """
    # 绘图
    color_list = [
        "#1A3CE6",
        "#D74325",
        "#1A8E0A",
        "#C31294"
    ]
    marker_list = [
        "o",
        "^",
        "s",
        "v"
    ]
    assert len(tick_inflight_list_list) == len(pattern_name_list)
    assert len(color_list) >= len(tick_inflight_list_list)
    
    plt.figure(figsize=(fig_a, fig_b))
    for idx in range(len(tick_inflight_list_list)):
        tick_inflight_list = tick_inflight_list_list[idx]
        tick_list = [t / 1000 for t, v in tick_inflight_list] # 单位 us
        vals_list = [v        for t, v in tick_inflight_list]
        if FIG_STYLE == "step":
            plt.step(tick_list, vals_list, where='post', linestyle='-', color=color_list[idx], linewidth=LINE_WIDTH, marker=marker_list[idx], ms=6, alpha=0.8)
        else:
            plt.plot(tick_list, vals_list, linestyle='-', color=color_list[idx], linewidth=LINE_WIDTH, marker=marker_list[idx], ms=6, alpha=0.8)

    # 添加标签和标题
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xlabel('time (us)', fontsize=38)
    plt.ylabel('#inflight WRs', fontsize=38)

    plt.yticks(y_tick_list)
    # 显示网格
    plt.grid(True, linestyle="--", alpha=0.6)
    # 自动调整布局并保存图片
    
    legend_handles = []
    for idx in range(len(pattern_name_list)):
        legend_line = Line2D([0], [0], color=color_list[idx], lw=LINE_WIDTH+2, marker=marker_list[idx], ms=15, label=pattern_name_list[idx])
        legend_handles.append(legend_line)
    plt.legend(handles=legend_handles, fontsize=38, ncol=3, loc='upper center', bbox_to_anchor=(0.5, 1.0))
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.savefig(fig_name+'.pdf', bbox_inches='tight', format='pdf', dpi=1000)
    print(f"Succeed to save the figure {fig_name}.pdf")
 
def get_nic_events_from_simai_log(log_file, src_idx_list):
    """
    输入: SimAI.log日志文件
    输出: 以PostSend Event和PollCq Event组成的列表
    """
    messages = defaultdict(lambda: {
        'src': None,
        'dst': None,
        'src_port': None,
        'size': None,
        'start_time': None,
        'end_time': None
    })

    pattern = r"发包事件\s+(\d+)\s+SendFlow\s+to\s+(\d+).*?src_port\s+(\d+)\s+size:\s+(\d+)\s+at the tick:\s+(\d+)"

    with open(log_file, 'r') as file:
        for line in file:
            # 匹配发包事件
            send_match = re.search(pattern, line)
            if send_match:
                src = int(send_match.group(1))
                dst = int(send_match.group(2))
                src_port = int(send_match.group(3))
                size = int(send_match.group(4))
                tick = int(send_match.group(5))
                key = (src, dst, src_port)
                messages[key]['src'] = src
                messages[key]['dst'] = dst
                messages[key]['src_port'] = src_port
                messages[key]['size'] = size
                messages[key]['start_time'] = tick

            # 匹配完成事件
            if "qp finish" in line:
                # print(2)
                src = line.split('src:')[1].split('did')[0].strip()
                did = line.split('did:')[1].split('port')[0].strip()
                port = line.split('port:')[1].split('total')[0].strip()
                finish_time = line.split('tick:')[1].strip().split(' ')[0].strip() 
                key = (int(src), int(did), int(port))
                
                if key in messages:
                    messages[key]['end_time'] = int(finish_time)

    # 将字典转换为列表
    result = []
    for key, message in messages.items():
        if message['start_time'] is not None and message['end_time'] is not None and message['src'] // 8 != message['dst'] // 8:
            # print("====")
            result.append({
                'src': message['src'],
                'dst': message['dst'],
                'src_port': message['src_port'],
                'size': message['size'],
                'start_time': message['start_time'],
                'end_time': message['end_time']
            })
    nic_events = []
    for msg in result:
        if msg['src'] in src_idx_list:
            nic_events.append(('PostSend', msg['start_time'], 1, 0))
            nic_events.append(('PollCq', msg['end_time'], 1, 0))
    nic_events.sort(key=lambda x: x[1])
    print("Length:",len(nic_events))
    return nic_events

def get_nic_events_from_astra_sim_logs(log_file, src_idx_list):
    events = []

    # 正则匹配 PostSend 类型
    postsend_pattern = re.compile(
        r'src (\d+) -> dst (\d+) size \d+ .+? at the tick (\d+) ns'
    )

    # 正则匹配 PollCq / finish 类型
    pollcq_pattern = re.compile(
        r'qp finish src (\d+) dst (\d+) .+? at the tick (\d+) ns'
    )

    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 匹配 PostSend 类型
            match_postsend = postsend_pattern.search(line)
            if match_postsend:
                src, dst, tick = match_postsend.groups()
                if int(src) in src_idx_list and int(src) // 8 != int(dst) // 8:
                    events.append(("PostSend", int(tick), 1, 0))
                else:
                    continue
            # 匹配 PollCq 类型
            match_pollcq = pollcq_pattern.search(line)
            if match_pollcq:
                src, dst, tick = match_pollcq.groups()
                if int(src) in src_idx_list and int(src) // 8 != int(dst) // 8:
                    events.append(("PollCq", int(tick), 1, 0))
                else:
                    continue
    return events



if __name__=="__main__":
    
    # 最终我们选择点到点之间有 2QPs 256M AllReduce 的case来绘图
    # 在motivation部分绘制 SimAI ASTRA-sim 和 NCCL 的 traffic pattern

    # ASTRA-sim
    astra_sim_events = get_nic_events_from_astra_sim_logs("./astra_sim_256M.log", [0])
    tick_inflight_astra_sim = get_num_inflight_vs_time(astra_sim_events, 'astra_sim')
    # SimAI
    simai_events = get_nic_events_from_simai_log("./SimAI_allreduce_256M.log", [0])
    tick_inflight_simai = get_num_inflight_vs_time(simai_events, 'simai')
    # NCCL
    nccl_nic_events = get_nic_events_from_nccltest_log("./NCCL_allreduce_256M.log", 240)
    tick_inflight_nccl = get_num_inflight_vs_time(nccl_nic_events, 'nccl')
    
    plot_num_inflight_N([tick_inflight_nccl, tick_inflight_simai, tick_inflight_astra_sim], ["NCCL", "SimAI", "ASTRA-sim"], "NCCL_SimAI_AstraSim_traffic_pattern", 20, 8, [0,2,4,6,8,10,12,14,16,18])