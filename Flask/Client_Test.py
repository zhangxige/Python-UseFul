import os
import requests
import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed


IP_ADRESS = 'http://127.0.0.1'
PORT = 5000


class server_api:
    def __init__(self):
        pass

    # 上传 json 数据
    def post_json(self, json_data: dict):
        route = '/alg/alg2'
        url = IP_ADRESS + ':' + str(PORT) + route
        response = requests.post(url, json=json_data)
        # headers = {'Content-Type': 'application/json'}
        # response = requests.post(url, data=json_data, headers=headers)
        print(response.text)  # 打印响应内容

    # 上传图片
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

    # 批量上传图片
    def post_img_list(self, image_urls: list):
        # 定义上传图片的函数
        def upload_image(image_url, upload_url):
            try:
                # 读取图片数据
                with open(image_url, 'rb') as f:
                    files = {'file': (image_url, f, 'image/jpeg')}
                    # 发送POST请求上传图片
                    response = requests.post(upload_url, files=files)
                return (image_url, response.status_code, response.text)
            except Exception as e:
                return (image_url, f"Error: {str(e)}")

        route = '/alg/alg3'
        upload_url = IP_ADRESS + ':' + str(PORT) + route
        # max_workers可以根据需要调整线程数
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(upload_image,
                                             image_url,
                                             upload_url): image_url
                             for image_url in image_urls}
            for future in as_completed(future_to_url):
                image_url = future_to_url[future]
                try:
                    result = future.result()
                    print(f'''Image URL: {image_url},
                              Status Code: {result[1]},
                              Response: {result[2]}''')
                except Exception as exc:
                    print(f'{image_url} generated an exception: {exc}')

    # 添加任务
    def post_work(self, json_data: dict):
        route = '/work/add'
        url = IP_ADRESS + ':' + str(PORT) + route
        response = requests.post(url, json=json_data)
        print(response.text)  # 打印响应内容

    # 查询任务
    def query_work(self):
        route = '/work/query'
        url = IP_ADRESS + ':' + str(PORT) + route
        response = requests.get(url)
        print(response.text)  # 打印响应内容


class Test_server_api(unittest.TestCase):
    # preparation init test
    @classmethod
    def setUpClass(cls):
        cls.test = server_api()

    def setUp(self):
        # 每一个测试前都会执行
        print('test begin!')

    def tearDown(self):
        # 每一个测试后都会执行
        print('end test!')

    def test_post_json(self):
        test = self.test
        data = {'name': 'value', 'world': 3000}  # 要发送的数据
        test.post_json(data)

    def test_post_image(self):
        test = self.test
        img_p = r'test.jpg'
        test.post_img(img_p)

    def test_post_images(self):
        test = self.test
        test_dir = r'./test_dir/'
        try:
            img_list = [os.path.join(test_dir, it)
                        for it in os.listdir(test_dir)
                        if it.endswith('.jpg')]
            test.post_img_list(img_list)
        except Exception as e:
            print(e)
    
    def test_post_work(self):
        test = self.test
        data = {'name': 'zxc', 'aaa': 'dfd'}
        test.post_json(data)


if __name__ == '__main__':
    # unittest.main()
    test = server_api()
    j = {'name': 'zccxc1', 'aaa': 'dfd'}
    test.post_work(j)
    j = {'name': 'zccxc2', 'aaa': 'dfd'}
    test.post_work(j)
    j = {'name': 'zccxc3', 'aaa': 'dfd'}
    test.post_work(j)
    j = {'name': 'zccxc4', 'aaa': 'dfd'}
    test.post_work(j)
    j = {'name': 'zccxc5', 'aaa': 'dfd'}
    test.post_work(j)
    test.query_work()
