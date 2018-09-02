# -*- coding: utf-8 -*-
# @Author: Li Qin
# @Date:   2018-07-12 13:03:37
# @Last Modified by:   Li Qin
# @Last Modified time: 2018-07-12 13:56:42
from PIL import Image
import os

'''
用法：
将所有需要拼接的图片放在文件夹tmp内
按照1,2,3...的顺序命名
'''

def pasted_size(images):
    max_width = 0
    total_height = 0
    for image in images:
        img = Image.open(image)
        w, h = img.size
        total_height += h
        if w > max_width:
            max_width = w
    return (max_width, total_height)

def read_images():
    base_url = "tmp"
    return sorted(os.path.join(base_url, img) \
           for img in os.listdir(base_url) \
           if not os.path.isdir(os.path.join(base_url, img)))

def paste_images():
    images = read_images()
    base_image = Image.new("RGB", pasted_size(images), (255,255,255,255))
    next_h = 0
    for image in images:
        img = Image.open(image)
        w, h = img.size
        base_image.paste(img, (0,next_h))
        next_h += h
    base_image.save("out.jpg")

if __name__ == "__main__":
    paste_images()
