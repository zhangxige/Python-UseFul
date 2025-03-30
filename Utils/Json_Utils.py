import json


# 写入json文件
def dump_json(filename: str, json_data: dict):
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=4)  # indent参数用于美化输出，使其更易读


# 从文件读取 json 文件
def load_json_file(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError as e:
        print(e)


# 字符串转字典
def load_json_str(json_str):
    data = json.loads(json_str)
    return data


if __name__ == '__main__':
    r = '{"name": "John Doe", "age": 30,' \
        ' "is_employee": true, "skills": ["Python", "Data Science"]}'
    res = load_json_str(r)
    print(res)
    pass