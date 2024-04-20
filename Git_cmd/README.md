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

- 查看分支
``` Git bash
// 查看本地分支
git branch

// 查看远程分支
git branch -r

// 查看所有分支
git branch -a
```

- 本地创建新的分支
``` Git bash
// git branch [branch name] e.g.:
git branch gh-dev
```

- 切换到新的分支
``` Git bash
// git checkout [branch name] e.g.:
git checkout gh-dev
```

- 创建+切换分支
``` Git bash
// git checkout -b [branch name] e.g.:
git checkout -b gh-dev
```

- 将新分支推送
``` Git bash
// 注意：origin 代表你的项目名字根据git branch查看
// git push origin [branch name] e.g.:
git push origin gh-dev
```

- 删除本地分支
``` Git bash
// 注意：origin 代表你的项目名字根据git branch查看
// git branch -d [branch name] e.g.:
git branch -d gh-dev
```

- 删除github远程分支
``` Git bash
// 注意：origin 代表你的项目名字根据git branch查看
// git push origin :[branch name] e.g.:
git push origin :gh-dev
```

- 常见问题汇总

#### 1、[git中出现error: Your local changes to the following files would be overwritten by merge的解决方案](https://blog.csdn.net/IT_SoftEngineer/article/details/107133284)

#### 2、[git中Updates were rejected because the tip of your current branch is behind解决方案](https://blog.csdn.net/IT_SoftEngineer/article/details/107133313)

