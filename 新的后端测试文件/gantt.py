#新的甘特图程序，会出一张图保存到一个路径下

import matplotlib
import matplotlib.pyplot as plt
import random
from matplotlib.font_manager import FontProperties

# 设置 matplotlib 使用 Agg 后端
matplotlib.use('Agg')

def drawGantt(T):
    # 指定字体路径
    font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'  # 选择一个支持中文的字体路径
    font_prop = FontProperties(fname=font_path)

    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC']  # 设置字体，以便支持中文显示
    fig, ax = plt.subplots(figsize=(10, 6))

    color_map = {}
    for machine_schedule in T:
        for task_data in machine_schedule[1:]:  # 跳过第一个元素，因为它是0
            job_idx = task_data[1]
            if job_idx not in color_map:
                color_map[job_idx] = (random.random(), random.random(), random.random())

    for machine_idx, machine_schedule in enumerate(T):
        for task_data in machine_schedule[1:]:  # 跳过第一个元素
            start_time, job_idx, _, end_time = task_data
            color = color_map[job_idx]
            ax.barh(machine_idx, end_time - start_time, left=start_time, height=0.4, color=color)
            ax.text((start_time + end_time) / 2, machine_idx, f'工件{job_idx+1}', ha='center', va='center', color='white', fontsize=9, fontproperties=font_prop)

    ax.set_yticks(range(len(T)))
    ax.set_yticklabels([f'机器{i+1}' for i in range(len(T))], fontproperties=font_prop)

    plt.xlabel("时间", fontproperties=font_prop)
    plt.title("甘特图", fontproperties=font_prop)
    # legend_handles = []
    # for job_idx, color in color_map.items():
    #     legend_handles.append(plt.Rectangle((0, 0), 1, 1, color=color, label=f'工件{job_idx+1}'))
    # plt.legend(handles=legend_handles, title='', prop=font_prop)

    # 保存图像到文件
    plt.savefig('gantt_chart.png')
    plt.close()
 