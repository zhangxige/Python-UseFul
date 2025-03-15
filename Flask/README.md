### Flask 项目demo
- 项目结构
``` shell
├── app/                   # 应用包
│   ├── __init__.py        # Flask 应用的初始化文件
│   ├── config.py          # 配置文件
│   ├── model.py           # 数据库模型
│   ├── model_views.py     # 视图函数
│   ├── test_db.db         # 项目测试的sqlite3数据库
│   ├── views/             # 其他视图（blueprint）
│   │   └── ...
│   ├── static/            # 静态文件（CSS, JavaScript, 图片等）
│   │   └── ...
│   ├── uplads/            # 可以上载的文件地址
│   │   └── ...
│   ├── templates/         # HTML 模板文件
│   │   └── ...
│   └── ...                # 其他包或模块
│
├── run.py                 # 启动脚本
├── requirements.txt       # 项目依赖
├── README.md              # 项目说明文件
└── .gitignore             # Git 忽略文件
```
