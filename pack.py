
from PIL import Image
import numpy
import os
import cv2
path = os.getcwd()

# img = cv2.imread(f'{path}/test_Image.png', cv2.IMREAD_GRAYSCALE)
img = Image.open(f'{path}/test_Image.png')

up_img = Image.new('L', (648, 12), 'white')  # 制作宽1024，长12的白条
down_img = Image.new('L', (648, 17), 'white')  # 制作宽1024，长17的白条
up_img.save(f'{path}/up.png')
down_img.save(f'{path}/down.png')

img.paste(up_img, (0, 0))  # 从左上角(0,0)处开始贴图
img.paste(down_img, (0, 495))  # 从下面开始贴图

img.save(f'{path}/chartlet.png')



