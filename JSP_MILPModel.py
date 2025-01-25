from gurobipy import Model, GRB, quicksum

def JSPModel(MacNum, job_count, job_seqs, production_time, V):
    model = Model("JSP")
    
    # 定义决策变量
    x = model.addVars(MacNum, job_count, vtype=GRB.CONTINUOUS, name="x")
    z = model.addVars(MacNum, job_count, job_count, vtype=GRB.BINARY, name="z")
    
    # 目标函数
    C_max = model.addVar(vtype=GRB.CONTINUOUS, name="C_max")
    model.setObjective(C_max, GRB.MINIMIZE)
    
    # 约束1
    for j in range(job_count):
        for h in range(1, len(job_seqs[j])):
            prev_machine = job_seqs[j][h - 1]
            curr_machine = job_seqs[j][h]
            model.addConstr(x[curr_machine, j] >= x[prev_machine, j] + production_time[prev_machine][j], name=f"seq_{j}_{h}")
    
    # 约束2
    for j in range(job_count):
        for h in range(1, len(job_seqs[j])):
            prev_machine = job_seqs[j][h - 1]
            curr_machine = job_seqs[j][h]
            model.addConstr(x[curr_machine, j] >= x[prev_machine, j] + production_time[prev_machine][j], name=f"seq_{j}_{h}")
    
    # 约束3
    for i in range(MacNum):
        for j in range(job_count):
            for k in range(j + 1, job_count):
                model.addConstr(x[i, j] >= x[i, k] + production_time[i][k] - V * z[i, j, k], name=f"constraint3_{i}_{j}_{k}")
                model.addConstr(x[i, k] >= x[i, j] + production_time[i][j] - V * (1 - z[i, j, k]), name=f"constraint3_{i}_{k}_{j}")
    
    # 约束4
    for j in range(job_count):
        last_machine = job_seqs[j][-1]
        model.addConstr(C_max >= x[last_machine, j] + production_time[last_machine][j], name=f"C_max_{j}")
    
    # 约束5
    for i in range(MacNum):
        for j in range(job_count):
            for k in range(job_count):
                model.addConstr(z[i, j, k] <= 1, name=f"z_bound_{i}_{j}_{k}")
                model.addConstr(z[i, j, k] >= 0, name=f"z_bound_{i}_{j}_{k}")
    
    # 设置参数
    model.params.TimeLimit = 10
    model.setParam('Threads', 20)
    model.update()
    
    return model
