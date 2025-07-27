# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask import Blueprint


# 数据库相关操作接口
class mid_process_api:
    mid = Blueprint("mid_process", __name__, url_prefix="/mid_process")

    def __init__(self):
        pass

    @mid.before_request
    def before_request():
        # print('Before request')
        pass

    @mid.after_request
    def after_request(response):
        # print('After request')
        return response

    @mid.teardown_request
    def teardown_request(exception):
        # print('Teardown request')
        pass

    @mid.route('/')
    def index():
        return 'Hello, World!'

    @mid.route('/land_list_info', methods=['GET', 'POST'])
    def land_list_info():
        data = request.json  # 这是一个字典类型，可以直接访问键值对
        print(data)
        return 'Hello, World!'
