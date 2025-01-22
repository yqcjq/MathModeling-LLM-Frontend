import requests
import json
from openai import OpenAI
from JSP_main import extract_jsp_data

from gurobipy import Model, GRB, quicksum
from gantt import drawGantt


# 设定请求的URL、Headers和数据
url = "http://222.20.98.39:3000/api/v1/chat/completions"


# AUTH_TOKEN="fastgpt-q1aJmIUVUFy7m8gYXoWxvXNPWcoSxAdk8JbDz4xdBFpY9AHQe9w6rd1GAkCgimKa"
# AUTH_TOKEN="fastgpt-j8MHw7D8prIVrmiJtIx4UlcZu0q6FGOQoactLjZgqGu4rdLT1cqKyt"
AUTH_TOKEN="fastgpt-yt38oh7XZBxmhdNYQcDGLJSG0LcbandiBrLPZpD6C1itNROWI8rpfOVg"

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",  # 假设你的令牌是Bearer类型的
    "Content-Type": "application/json"  # 通常需要设置内容类型为JSON
}

# 输入问题
input = "创建一个作业车间调度模型。目标函数为最小化最大完工时间。"

# 开始第一步--------------------------------------------------------------------------------------------
# 设置第一步的提示词

file_path = 'prompt_for_1.txt'
prompt_for_1 = ''
with open(file_path, 'r', encoding='utf-8') as f:
    prompt_for_1 = f.read()

prompt_for_1 = prompt_for_1.replace("{input}", input)

data = {
    # "chatId": "f",
    "stream": False,
    "detail": False,
    "messages": [
        # {'role': 'system', 'content': '假设你是一个调度专家'},
        {'role': 'user', 'content': prompt_for_1}
    ]

}

# 发送POST请求
response = requests.post(url, headers=headers, data=json.dumps(data))
 
# 解析响应体为JSON并提取content字段的内容
try:
    response_data = response.json()
    choices = response_data.get("choices", [])
    if choices:
        message = choices[0].get("message", {})
        content = message.get("content", "No content found in the response")
        # 从回复的内容中拿到约束描述
        constraint_description = content
        print('成功提取约束描述')
    else:
        print("No choices found in the response")
except json.JSONDecodeError:
    print("Failed to decode response as JSON")
except Exception as e:
    print(f"An error occurred: {e}")

# 开始第二步--------------------------------------------------------------------------------------------
# 设置第二步的提示词

file_path = 'prompt_for_2.txt'
prompt_for_2 = ''
with open(file_path, 'r', encoding='utf-8') as f:
    prompt_for_2 = f.read()

prompt_for_2 = prompt_for_2.replace("{input}", input)
prompt_for_2 = prompt_for_2.replace("{constraint_description}", constraint_description)

data = {
    # "chatId": "f",
    "stream": False,
    "detail": False,
    "messages": [
        # {'role': 'system', 'content': '假设你是一个调度专家'},
        {'role': 'user', 'content': prompt_for_2}
    ]

}

# 发送POST请求
response = requests.post(url, headers=headers, data=json.dumps(data))

# 解析响应体为JSON并提取content字段的内容
try:
    response_data = response.json()
    choices = response_data.get("choices", [])
    if choices:
        message = choices[0].get("message", {})
        content = message.get("content", "No content found in the response")
        # 从回复的内容中拿到符号列表和公式
        # 找到两个标志的起始索引
        start_var_idx = content.index("//参数列表")
        end_var_idx = content.index("//公式构建", start_var_idx)  # 从start_var_idx之后查找
        
        # 提取两个字符串
        variable1 = content[start_var_idx+6:end_var_idx].strip()  # 使用strip()去除可能的首尾空白字符
        formula1 = content[end_var_idx+6:].strip()  # 从//公式构建开始到字符串末尾
        print('成功提取公式与变量')
    else:
        print("No choices found in the response")
except json.JSONDecodeError:
    print("Failed to decode response as JSON")
except Exception as e:
    print(f"An error occurred: {e}")

# 开始第三步--------------------------------------------------------------------------------------------
# 输入符号列表和公式，直接调用第三步的方法，得到最终结果
def model_inference(prompt):
    """
    使用本地模型进行推理。
    Args:
        prompt (str): 提示词内容
    Returns:
        str: 模型推理的输出
    """
    try:
        response = client.chat.completions.create(
            model="glm-4",  # 根据实际模型名称调整
            # model="Meta-Llama-3-8B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=8192,
            temperature=0
        )
        # 如果返回成功，提取结果
        if response and response.choices:
            # 修改此处，直接获取message内容
            return response.choices[0].message.content
        else:
            return "推理出错或无响应"
    except Exception as e:
        return f"推理过程中发生错误: {str(e)}"
def write_output_to_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
def output_code(path,output_code_path):
    """更新输出的代码到测试文件"""
    with open(path, 'r',encoding='utf-8') as file:
        lines = file.readlines()
        start_index =0
        #删除开头冗余的部分
        for index, line in enumerate(lines):
            if line.strip().endswith('```python'):
                start_index = index+1
                break
        lines = lines[start_index:]
        #删除结尾冗余的部分
        if lines[-1] == '```':
            lines = lines[:-1]
    with open(output_code_path, 'w') as file:
        file.writelines(lines) 
    print("代码已更新")
#调用GLM
base_url = "http://127.0.0.1:8020/v1/"
client = OpenAI(api_key="EMPTY", base_url=base_url)
file_path = 'prompt_for_3.txt'
prompt_code = ''
with open(file_path, 'r', encoding='utf-8') as f:
    prompt_code = f.read()

#读取提示词的程序
prompt_code = prompt_code.replace("{variable}", variable1)
prompt_code = prompt_code.replace("{formula}", formula1)
output_file_path = "finall_prompt.txt"#输出最后的提示词
write_output_to_file(output_file_path, prompt_code)


#让GLM输出代码
inference_result = model_inference(prompt_code)    
# 3保存推理结果到 step4_output.txt
output_file_path = "step4_output.txt"
write_output_to_file(output_file_path, inference_result)
print('成功建立MILP模型')
#更新到测试代码
output_code('step4_output.txt','JSP_MILPModel.py')
print(f"推理结果已保存到 {output_file_path}")

import JSP_MILPModel

#调用数据处理函数
num_machines, num_jobs, job_seqs, production_time,V = extract_jsp_data('JSP_data.txt')
#运行JSPModel
model = JSP_MILPModel.JSPModel(num_jobs, num_machines, job_seqs, production_time, V)
model.optimize()
# 打印结果
if model.status == GRB.OPTIMAL:
        print("Optimization finished.")
        print("OBJ: ", model.objVal)
        print()
else:
    print("No optimal solution found.")

#绘制甘特图
if model.status == GRB.OPTIMAL:
        # 初始化 T 矩阵
        T = [[[0]] for _ in range(num_machines)]
        for j in range(num_jobs):  # 遍历所有工件
            for i in range(num_machines):  # 遍历所有机器
                # 构建变量名称
                var_name = f"x[{i},{j}]"
                # 获取工件 j 在机器 i 上的开始加工时间
                start_time = model.getVarByName(var_name).X  # 使用 getVarByName 方法
                if start_time > 0:  # 如果开始时间大于0，表示该工件在该机器上有加工任务
                    # 计算结束时间
                    end_time = start_time + production_time[i][j]
                    # 将开始时间、机器号、工件号、结束加工时间添加到 T 矩阵
                    T[i].append([start_time, j, i, end_time])

        # 打印 T 矩阵
        with open('gantt.txt', 'w', encoding='utf-8') as file:
            file.write(str(T))

        drawGantt(T)

