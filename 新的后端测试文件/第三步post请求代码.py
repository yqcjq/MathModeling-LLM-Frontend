import re
import os
import matplotlib.pyplot as plt
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

#这个函数从后面第三步那里提到最前面
def write_output_to_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# latex转公式图片函数
def latex_to_image(latex_formula, filename='formula.png', dpi=300):
    # 使用matplotlib绘制公式
    fig = plt.figure(figsize=(10, 1))  # 设置画布大小
    ax = fig.add_subplot(111)
    ax.axis('off')  # 关闭坐标轴
    
    # 在画布上绘制公式
    ax.text(0.5, 0.5, f'${latex_formula}$', fontsize=20, ha='center', va='center')
    
    # 将画布保存为图片
    plt.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)

# # 输入问题
# input = "创建一个作业车间调度模型。"

# # 开始第一步--------------------------------------------------------------------------------------------
# # 设置第一步的提示词

# file_path = 'prompt_for_1.txt'
# prompt_for_1 = ''
# with open(file_path, 'r', encoding='utf-8') as f:
#     prompt_for_1 = f.read()

# prompt_for_1 = prompt_for_1.replace("{input}", input)

# data = {
#     # "chatId": "f",
#     "stream": False,
#     "detail": False,
#     "messages": [
#         # {'role': 'system', 'content': '假设你是一个调度专家'},
#         {'role': 'user', 'content': prompt_for_1}
#     ]

# }

# # 发送POST请求
# response = requests.post(url, headers=headers, data=json.dumps(data))
 
# # 解析响应体为JSON并提取content字段的内容
# try:
#     response_data = response.json()
#     choices = response_data.get("choices", [])
#     if choices:
#         message = choices[0].get("message", {})
#         content = message.get("content", "No content found in the response")
#         # 从回复的内容中拿到约束描述
#         # 这里是一整段的约束描述
#         constraint_description = content
#         print('成功提取约束描述')
#         #将约束描述保存到constraint_description.txt中
#         output_file_path = "constraint_description.txt"
#         write_output_to_file(output_file_path, constraint_description)
        
#         #打开constraint_description.txt文件，并获取分条显示的列表
#         file_path = 'constraint_description.txt'
#         with open(file_path, 'r', encoding='utf-8') as f:
#             constraint_description = f.read()
#         constraint_description_pattern = re.compile(r'约束(\d+)：(.*?)(?=\n约束\d+|$)', re.DOTALL)
#         #前端界面接口，constraint_description_list列表，每一条都是一个约束+++++++++++++++++++++++++++++++++前端看这里++++++++++++++++++++++
#         constraint_description_list = [f"约束{match.group(1)}：{match.group(2).strip()}" for match in constraint_description_pattern.finditer(constraint_description)]

#     else:
#         print("No choices found in the response")
# except json.JSONDecodeError:
#     print("Failed to decode response as JSON")
# except Exception as e:
#     print(f"An error occurred: {e}")

# # 开始第二步--------------------------------------------------------------------------------------------
# # 设置第二步的提示词

# file_path = 'prompt_for_2.txt'
# prompt_for_2 = ''
# with open(file_path, 'r', encoding='utf-8') as f:
#     prompt_for_2 = f.read()
# #补充：打开constraint_description.txt文件读取constraint_description
# prompt_for_2 = prompt_for_2.replace("{input}", input)
# prompt_for_2 = prompt_for_2.replace("{constraint_description}", constraint_description)

# data = {
#     # "chatId": "f",
#     "stream": False,
#     "detail": False,
#     "messages": [
#         # {'role': 'system', 'content': '假设你是一个调度专家'},
#         {'role': 'user', 'content': prompt_for_2}
#     ]

# }

# # 发送POST请求
# response = requests.post(url, headers=headers, data=json.dumps(data))

# # 解析响应体为JSON并提取content字段的内容
# try:
#     response_data = response.json()
#     choices = response_data.get("choices", [])
#     if choices:
#         message = choices[0].get("message", {})
#         content = message.get("content", "No content found in the response")
#         # 从回复的内容中拿到符号列表和公式
#         # 找到两个标志的起始索引
#         start_var_idx = content.index("//参数列表")
#         end_var_idx = content.index("//公式构建", start_var_idx)  # 从start_var_idx之后查找
        
#         # 提取两个字符串，这里是整段变量、整段公式
#         variable = content[start_var_idx+6:end_var_idx].strip()  # 使用strip()去除可能的首尾空白字符
#         formula = content[end_var_idx+6:].strip()  # 从//公式构建开始到字符串末尾
#         print('成功提取公式与变量')

#         #将变量保存到variable.txt中
#         output_file_path = "variable.txt"
#         write_output_to_file(output_file_path, variable)

#         #将公式保存到formula.txt中
#         output_file_path = "formula.txt"
#         write_output_to_file(output_file_path, formula)
        
#         #打开formula.txt文件，并获取分条显示的列表
#         file_path = 'formula.txt'
#         with open(file_path, 'r', encoding='utf-8') as f:
#             formula = f.read()

#         # 使用正则表达式匹配公式和约束编号
#         pattern = re.compile(r"\\begin\{equation\}(.*?)\\end\{equation\}\s*#\(约束(\d+)\)", re.DOTALL)

#         # 创建一个字典来存储具有相同约束编号的公式
#         formulas_dict = {}

#         # 查找所有匹配项
#         matches = pattern.findall(formula)

#         # 将匹配项添加到字典中
#         for formula, constraint_number in matches:
#             formula_with_env = f"\\begin{{equation}}{formula.strip()}\\end{{equation}}"
#             if constraint_number not in formulas_dict:
#                 formulas_dict[constraint_number] = []
#             formulas_dict[constraint_number].append(formula_with_env)

#         # 创建一个临时目录来存储生成的图片文件，这里要你手动建一个文件夹名为fomula_photo
#         temp_dir = "fomula_photo"

#         # 遍历 formulas_dict，为每个公式生成图片
#         for constraint_number, formulas in formulas_dict.items():
#             for idx, single_formula in enumerate(formulas):
#                 # 为每个公式创建一个唯一的文件名
#                 image_file = os.path.join(temp_dir, f"formula_{constraint_number}_{idx + 1}.png")
                
#                 # 使用 latex_to_image 函数生成图片
#                 latex_to_image(single_formula, filename=image_file, dpi=300)
                
#                 # 打印生成的图片文件路径
#                 print(f"Generated image for formula {idx + 1} of constraint {constraint_number}: {image_file}")
#         # 前端界面接口，公式用这些图片表示+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++前端看这里+++++++++++++++++++++++++++++
#         # 例如图片名formula_3_1.png表示约束3的第1个公式，同一个约束底下可能有多个公式，前端界面要注意放一块+++++++++++前端看这里+
#     else:
#         print("No choices found in the response")
# except json.JSONDecodeError:
#     print("Failed to decode response as JSON")
# except Exception as e:
#     print(f"An error occurred: {e}")

# #在第三步之前，可以修改约束和公式
# #1增加推荐约束或自定义约束、2删除约束、3修改约束、4最后点击执行+++++++++++++++++++++++++++++++++++++++++++++++++++前端看这里+++++++++++++++++++++++++++++
# #1增加约束功能，点击约束推荐，将新的约束添加到constraint_description.txt文件的末尾
# """
# #接口，点击的约束推荐的内容被保存到变量new_constraint中
# new_constraint = "我是新的约束"#这个是接口，把它换掉+++++++++++++++++++++++++++++++++++++++++++++++++前端看这里+++++++++++++++++++++++++++++

# # 读取文件内容
# with open('constraint_description.txt', 'r', encoding='utf-8') as file:
#     lines = file.readlines()
 
# # 提取当前的最大约束编号
# max_constraint_number = 0
# for line in lines:
#     if line.startswith('约束 '):
#         number_str = line.split('：')[0].split(' ')[-1]
#         if number_str.isdigit():
#             max_constraint_number = max(max_constraint_number, int(number_str))
 
# # 生成新的约束编号
# new_constraint_number = max_constraint_number + 1
 
# # 构造新的约束行
# new_constraint_line = f"约束 {new_constraint_number}：{new_constraint}\n"
 
# # 将新的约束行添加到文件内容中（这里选择在文件末尾添加）
# lines.append(new_constraint_line)
 
# # 将更新后的内容写回文件
# with open('constraint_description.txt', 'w', encoding='utf-8') as file:
#     file.writelines(lines)
# """
# #2前端用户可删除某些条约束和公式（在各条约束显示那里设置叉号），当用户点击叉掉，删除对应的约束和公式，并将结果更新到constraint_description.txt和formula.txt中
# #3修改约束（如何操作？）
# #4执行更改，再次执行第二步获取公式（思路：把第二步打包）
# #补充：重建模型，怎么实现？

# # 开始第三步--------------------------------------------------------------------------------------------
# # 输入符号列表和公式，直接调用第三步的方法，得到最终结果
# def model_inference(prompt):
#     """
#     使用本地模型进行推理。
#     Args:
#         prompt (str): 提示词内容
#     Returns:
#         str: 模型推理的输出
#     """
#     try:
#         response = client.chat.completions.create(
#             model="glm-4",  # 根据实际模型名称调整
#             # model="Meta-Llama-3-8B-Instruct",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=8192,
#             temperature=0
#         )
#         # 如果返回成功，提取结果
#         if response and response.choices:
#             # 修改此处，直接获取message内容
#             return response.choices[0].message.content
#         else:
#             return "推理出错或无响应"
#     except Exception as e:
#         return f"推理过程中发生错误: {str(e)}"


def model_inference(prompt, auth_token = "EMPTY"):
    """
    使用本地模型进行推理。
    Args:
        prompt (str): 提示词内容
        auth_token (str): 认证令牌
    Returns:
        str: 模型推理的输出
    """
    url = "http://222.20.98.39:8020/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {auth_token}",  # 假设你的令牌是Bearer类型的
        "Content-Type": "application/json"  # 通常需要设置内容类型为JSON
    }
    data = {
        "model": "glm-4",  # 根据实际模型名称调整
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 8192,
        "temperature": 0
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            # 解析响应，这里假设响应是 JSON 格式，并且结果在某个键下，需要根据实际响应修改
            result = response.json()
            print("成功编写代码")
            if 'choices' in result and result['choices']:
                return result['choices'][0]['message']['content']
            else:
                return "推理出错或无响应"
        else:
            return f"请求失败，状态码: {response.status_code}"
    except Exception as e:
        return f"推理过程中发生错误: {str(e)}"



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
# #调用GLM
# base_url = "http://222.20.98.39:8020/v1/"
# client = OpenAI(api_key="EMPTY", base_url=base_url)
# file_path = 'prompt_for_3.txt'
file_path = 'finall_prompt.txt'
prompt_code = ''
with open(file_path, 'r', encoding='utf-8') as f:
    prompt_code = f.read()

# #读取提示词的程序
# prompt_code = prompt_code.replace("{variable}", variable)
# prompt_code = prompt_code.replace("{formula}", formula)
# output_file_path = "finall_prompt.txt"#输出最后的提示词
# write_output_to_file(output_file_path, prompt_code)


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

# #绘制甘特图
# if model.status == GRB.OPTIMAL:
#         # 初始化 T 矩阵
#         T = [[[0]] for _ in range(num_machines)]
#         for j in range(num_jobs):  # 遍历所有工件
#             for i in range(num_machines):  # 遍历所有机器
#                 # 构建变量名称
#                 var_name = f"x[{i},{j}]"
#                 # 获取工件 j 在机器 i 上的开始加工时间
#                 start_time = model.getVarByName(var_name).X  # 使用 getVarByName 方法
#                 if start_time > 0:  # 如果开始时间大于0，表示该工件在该机器上有加工任务
#                     # 计算结束时间
#                     end_time = start_time + production_time[i][j]
#                     # 将开始时间、机器号、工件号、结束加工时间添加到 T 矩阵
#                     T[i].append([start_time, j, i, end_time])

#         # 打印 T 矩阵
#         with open('gantt.txt', 'w', encoding='utf-8') as file:
#             file.write(str(T))

#         drawGantt(T)

