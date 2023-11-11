import os
import shutil
from tqdm import tqdm
from enum import Enum


class File_Type(Enum):
    '''
        定义文件检索类型
    '''
    TOPFILES = 0  # 最上层的文件
    ALLFILES = 1  # os.walk原始数据
    TOPDESFILES = 2  # 过滤自定义类型
    TOPKEYDESFILES = 3  # 过滤自定义类型并包含某些关键词


class File_OP():
    '''
        文件相关操作类
    '''
    @staticmethod
    def Filter_Des(files: list[str], des: tuple[str]):
        return (it for it in list(files) if it.endswith(des))

    @staticmethod
    def Filter_Des_Key(files: list[str], des: tuple, keys: tuple[str]):
        for it in list(files):
            if it.endswith(des):
                for k in keys:
                    if k.lower() in it.lower():
                        yield it
                        break
                    else:
                        pass

    @classmethod
    def Get_FileList(cls, filedir: str, current: File_Type, **args):
        ''' 基于os.walk 获取文件夹内容'''
        if not os.path.exists(filedir):
            print(f'{filedir},目标目录不存在！')
            return []
        res = os.walk(filedir, topdown=True)
        if current == File_Type.TOPFILES:
            return list(res)[0]
        elif current == File_Type.ALLFILES:
            return list(res)
        elif current == File_Type.TOPDESFILES:
            filter_res = list(File_OP.Filter_Des(
                list(res)[0][2],
                args['types'])
                )
            return filter_res
        elif current == File_Type.TOPKEYDESFILES:
            filter_res = list(File_OP.Filter_Des_Key(
                list(res)[0][2],
                args['types'],
                args['keys'])
                )
            return filter_res
        else:
            pass
 
    @classmethod
    def Batch_FileCopy(cls, src_filedir, dst_filedirt):
        src_list = (os.path.join(src_filedir, it) for it in os.listdir(src_filedir))
        for src_file in tqdm(src_list):
            try:
                shutil.copy2(src_file, dst_filedirt)
                # print(src_file, '文件复制成功！')
            except FileNotFoundError:
                print(src_file, '源文件不存在！')
            except PermissionError:
                print(src_file, '无法访问源文件或目标文件夹！')


# 测试一
def test_findfile():
    opt = File_Type.TOPKEYDESFILES
    types = ('.py', '.txt',)
    keys = ('util',)
    file_dir = r''
    test = File_OP()
    res = test.Get_FileList(file_dir, opt, types=types, keys=keys)
    print(res)


# 测试二
def test_copyfiles():
    src_dir = r''
    dst_dir = r''
    test = File_OP()
    test.Batch_FileCopy(src_dir, dst_dir)


if __name__ == '__main__':
    test_findfile()
    test_copyfiles()

