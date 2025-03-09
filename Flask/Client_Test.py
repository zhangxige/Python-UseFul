import requests


IP_ADRESS = 'http://127.0.0.1'
PORT = 5000


class server_api:
    def __init__(self):
        pass

    def post_json(self, json_data: dict):
        route = '/alg/alg2'
        url = IP_ADRESS + ':' + str(PORT) + route
        response = requests.post(url, json=json_data)
        # headers = {'Content-Type': 'application/json'}
        # response = requests.post(url, data=json_data, headers=headers)
        print(response.text)  # 打印响应内容

    def post_img(self, img_path: str):
        route = '/alg/alg3'
        url = IP_ADRESS + ':' + str(PORT) + route
        # 构建包含图片文件的multipart/form-data请求体
        try:
            with open(img_path, 'rb') as f:
                files = {'file': (img_path, f, 'image/jpeg')}
                # 发送POST请求上传图片
                response = requests.post(url, files=files)
                # 输出响应内容
                print(response.text)
        except FileNotFoundError:
            print("错误：文件不存在。")


if __name__ == '__main__':
    test = server_api()
    data = {'name': 'value', 'world': 3000}  # 要发送的数据
    test.post_json(data)
    img_p = r'test.jpg'
    test.post_img(img_p)
    pass
