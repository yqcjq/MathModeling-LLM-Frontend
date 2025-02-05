import numpy as np

def extract_jsp_data(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # 初始化 job_seqs 和 production_time
    first_line = lines[0].strip().split()
    num_machines = int(first_line[0])
    num_jobs = int(first_line[1])
    job_seqs = []  # 存储每个作业的加工顺序
    production_time = [[0 for _ in range(num_jobs)] for _ in range(num_machines)]
    V = 0
    for job, line in enumerate(lines[1:]):
        parts = line.strip().split()
        job_seqs_temp =[]
        if not parts:
            continue  # 跳过空行
        for i in range(int(len(parts)/2)):
            machine = int(parts[2*i])
            time = int(parts[2*i+1])
            job_seqs_temp.append(machine)
            production_time[machine][job]=time
            V += int(parts[2*i+1])
        job_seqs.append(job_seqs_temp)# 存储作业顺序
    job_seqs=np.array(job_seqs)
    production_time = np.array(production_time)
    return num_machines, num_jobs, job_seqs, production_time, V

