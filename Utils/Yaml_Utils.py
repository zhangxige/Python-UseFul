import yaml
import os


if __name__ == '__main__':
    # 获取当前脚本所在文件夹路径
    curPath = os.path.dirname(os.path.realpath(__file__))
    # 获取yaml文件路径
    ymlPath = os.path.join(curPath, "cfg/cfg.yml")

    # 用open方法打开直接读取
    with open(ymlPath, 'w') as f:
        a = {'name': 'Tom',
             'race': 'cat',
             'traits': ['Two_Hand', 'Two_Eye']
             }
        yaml.safe_dump(a, f, default_flow_style=False)

    # 用open方法打开直接读取
    with open(ymlPath, 'r') as f:
        cfg = f.read()
        # 读取的结果是 字符串
        print(type(cfg))
        print(cfg)
        # 读取的结果是 转字典
        res = yaml.safe_load(cfg)
        print(type(res))
        print(res)
