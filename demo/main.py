from flask import Flask, jsonify, request
import os
from JSP_main import extract_jsp_data
from gurobipy import GRB

app = Flask(__name__)

# 日志文件路径
log_file_path = 'milp_jsp.log'

# 确保日志文件存在
if not os.path.exists(log_file_path):
    raise FileNotFoundError(f"The log file does not exist: {log_file_path}")


@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        # 读取日志文件内容
        with open(log_file_path, 'r', encoding='utf-8') as file:
            logs = file.readlines()

        # 将日志文件内容转换为列表（去除每行末尾的换行符）
        log_entries = [line.strip() for line in logs]

        # 直接返回 JSON 响应
        return jsonify({"logs": log_entries})
    except Exception as e:
        # 如果发生错误，返回 500 状态码和错误信息（注意：这里 Flask 会自动将状态码设置为 500）
        return jsonify({"error": str(e)}), 500


def output_code(path, output_code_path):
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


def write_output_to_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


@app.route('/inference', methods=['POST'])
def get_inference_result():
    # 由于推理可能涉及敏感数据或大量数据，通常使用 POST 请求来发送 params
    try:
        # 从请求体中获取 JSON 数据
        params = request.get_json()
        if not params:
            return jsonify({"error": "No input data provided"}), 400

        inference_result = params.get('inference_result')
        if inference_result is None:
            return jsonify({"error": "Missing 'inference_result' in input data"}), 400
        # 调用推理函数
        # inference_result = infer(params)
        output_file_path = "step4_output.txt"
        write_output_to_file(output_file_path, inference_result)
        output_code('step4_output.txt', 'JSP_MILPModel.py')

        import JSP_MILPModel
        # 调用数据处理函数
        num_machines, num_jobs, job_seqs, production_time, V = extract_jsp_data('JSP_data.txt')
        # 运行JSPModel
        model = JSP_MILPModel.JSPModel(num_jobs, num_machines, job_seqs, production_time, V)
        model.setParam(GRB.Param.LogFile,"milp_jsp.log")
        model.optimize()
        # 打印结果
        if model.status == GRB.OPTIMAL:
            print("Optimization finished.")
            print("OBJ: ", model.objVal)
            print()
        else:
            print("No optimal solution found.")

        # 返回推理结果
        return jsonify(inference_result)
    except Exception as e:
        # 如果发生错误，返回 500 状态码和错误信息
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5050)