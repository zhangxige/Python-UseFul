import os
from PIL import Image
import cv2
import shutil
import numpy as np
import zipfile
from tqdm import tqdm
import pillow_heif


# 复制操作
def copy_file(source_path, des_path):
    if not os.path.exists(des_path):
        shutil.copy2(source_path, des_path)
    else:
        pass


# 读图片文件， 这种方式能读取路径中含有中文的图像文件
def imread(path):
    image_array = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)  #
    return image_array


# 存图片文件
def imsave(path, image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imencode('.png', image)[1].tofile(path)


# 判断是否是苹果手机拍摄的实时照片
def is_livp(file_name):
    if (os.path.splitext(file_name)[-1] == ".livp" or
            os.path.splitext(file_name)[-1] == ".LIVP"):
        return True
    else:
        return False


def read_image_file_rb(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    return file_data


# livp 格式转jpg
def livp_to_jpg(img_item, img_source, livp_to_jpg_dir):
    img_id = img_item.split('.')[0]
    livp_zip_name = os.path.join(livp_to_jpg_dir, img_id+'.zip')
    # 将文件复制成zip归档的形式
    copy_file(img_source, livp_zip_name)

    heic_name = ''
    with zipfile.ZipFile(livp_zip_name) as zf:
        for zip_file_item in zf.namelist():
            if zip_file_item.split('.')[-1] == 'heic':
                zf.extract(zip_file_item, livp_to_jpg_dir)
                heic_name = zip_file_item
    # delete the zip file
    os.remove(livp_zip_name)
    heic_img_path = os.path.join(livp_to_jpg_dir, heic_name)

    heif_file = pillow_heif.read_heif(heic_img_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
    )

    jpg_save_path = os.path.join(livp_to_jpg_dir, img_id + '.jpg')
    image.save(jpg_save_path, format="jpeg")

    os.remove(heic_img_path)  # delete the zip file


# heic 格式转jpg
def heic_to_jpg(img_item, img_source, livp_to_jpg_dir):
    img_id = img_item.split('.')[0]
    heif_file = pillow_heif.read_heif(img_source)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
    )

    jpg_save_path = os.path.join(livp_to_jpg_dir, img_id + '.jpg')
    image.save(jpg_save_path, format="jpeg")


# 批处理
def Batch_heic_to_jpg():
    heic_dir = r'C:\Users\zhangxige\Desktop\结婚照\满意视频素材'
    heic_to_jpg_dir = r'C:\Users\zhangxige\Desktop\结婚照\满意视频素材'

    img_list = os.listdir(heic_dir)
    for img_item in tqdm(img_list):
        # print(img_item)
        img_source = os.path.join(heic_dir, img_item)
        if img_item.endswith('.heic'):
            heic_to_jpg(img_item, img_source, heic_to_jpg_dir)
        else:
            pass


# 批处理
def Batch_livp_to_jpg():
    livp_dir = r'C:\Users\zhangxige\Downloads\来自：iPhone'
    livp_to_jpg_dir = r'C:\Users\zhangxige\Downloads\Iphone'

    img_list = os.listdir(livp_dir)
    for img_item in tqdm(img_list):
        # print(img_item)
        img_source = os.path.join(livp_dir, img_item)
        if img_item.endswith('.livp'):
            livp_to_jpg(img_item, img_source, livp_to_jpg_dir)
        else:
            # copy_file(img_source, livp_to_jpg_dir)
            pass


if __name__ == '__main__':
    Batch_heic_to_jpg()
    # Batch_livp_to_jpg()
