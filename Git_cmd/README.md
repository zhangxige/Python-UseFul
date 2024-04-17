- Git 初始化
```shell
git init
```
- 显示当前仓库下文件
```shell
ls -a
```
- 显示当前仓库状态
```Shell
git status
```

- 在本地通过以下命令可以给远程仓库起别名：
``` Git bash
git remote add name url
e.g. 
git remote add python-project https://github.com/zhangxige/Python-UseFul.git

```

- git 查看已配置的远程仓库地址
``` Git bash
git remote -v
```

- 向本地仓库删除文件
``` Git bash
git rm sommefile/folder
e.g.
$ git rm Git_cmd/
```

- 向本地仓库添加文件
``` Git bash
git add sommefile/folder
e.g.
$ git add Git_cmd/
```

- 向本地仓库添加文件
``` Git bash
git commit -m "someinfo"
```

- 向远程仓库推送分支
``` Git bash
git push -u Python-UseFul "main"
```

- 常见问题汇总

#### 1、[git中出现error: Your local changes to the following files would be overwritten by merge的解决方案](https://blog.csdn.net/IT_SoftEngineer/article/details/107133284)

#### 2、[git中Updates were rejected because the tip of your current branch is behind解决方案](https://blog.csdn.net/IT_SoftEngineer/article/details/107133313)

