# import re
# import requests
# import json
# from JSP_main import extract_jsp_data
#
# from gurobipy import Model, GRB, quicksum
#
# def output_code(path,output_code_path):
#     """更新输出的代码到测试文件"""
#     with open(path, 'r',encoding='utf-8') as file:
#         lines = file.readlines()
#         start_index =0
#         #删除开头冗余的部分
#         for index, line in enumerate(lines):
#             if line.strip().endswith('```python'):
#                 start_index = index+1
#                 break
#         lines = lines[start_index:]
#         #删除结尾冗余的部分
#         if lines[-1] == '```':
#             lines = lines[:-1]
#     with open(output_code_path, 'w') as file:
#         file.writelines(lines)
#     print("代码已更新")
#
# def write_output_to_file(file_path, content):
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.write(content)
#
# #让GLM输出代码
# # 3保存推理结果到 step4_output.txt
# output_file_path = "step4_output.txt"
# write_output_to_file(output_file_path, inference_result)
# print('成功建立MILP模型')
# #更新到测试代码
# output_code('step4_output.txt','JSP_MILPModel.py')
# print(f"推理结果已保存到 {output_file_path}")
#
# import JSP_MILPModel
#
# #调用数据处理函数
# num_machines, num_jobs, job_seqs, production_time,V = extract_jsp_data('JSP_data.txt')
# #运行JSPModel
# model = JSP_MILPModel.JSPModel(num_jobs, num_machines, job_seqs, production_time, V)
#
# model.optimize()
# # 打印结果
# if model.status == GRB.OPTIMAL:
#         print("Optimization finished.")
#         print("OBJ: ", model.objVal)
#         print()
# else:
#     print("No optimal solution found.")
#
