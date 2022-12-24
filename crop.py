import os 
path_img = '/media/pc/hengda1t/hengda/e4e_eg3d/data/sister_input/work2.jpg'
from PIL import Image
import math
import numpy as np
from argparse import ArgumentParser


IMAGE_EXTENSION = ['.png','.jpg','.PNG','.JPG','.jpeg']

def crop_img(im):
    img_size = im.size # (w,h)
    print("图片宽度和高度分别是{}".format(img_size))
    wide,height = img_size[0],img_size[1]
    assert (height / wide) > 0
    ratios = round(height/wide) # 高宽比例。
    n = math.ceil(math.sqrt(ratios)) # 想要切割成多少张小图片
    each_height =  math.ceil(height/n) #每层高度
    img_array=''
    img_array2=''
    for i in range(n):
        h = each_height *(i+1)
        upper = i *  each_height
        region = im.crop((0, upper, wide, h))  # 因为元组，勿忘里面加层括号
        if i == 0:
            img_array = np.array(region)  # 转化为np array对象
        if i > 0:
            img_array2 = np.array(region)
            img_array = np.concatenate((img_array, img_array2), axis=1)  # 横向拼接
    return Image.fromarray(img_array)

def load_img(img_path,output_path):
    if os.path.isdir(img_path): #若是文件夹路径
        files = os.listdir(img_path)
        assert len(files)>0  #文件数必须大于0
        for file in files:
            print(f'now print is {file}')
            if file[-4:] in IMAGE_EXTENSION: #图片
                im = Image.open(os.path.join(img_path,file))
                result = crop_img(im)
                result.save(os.path.join(output_path,file))
    else: #直接单图输入
        print(f'now print is {os.path.basename(img_path)}')
        if img_path[-4:] in IMAGE_EXTENSION: #图片
            im = Image.open(img_path)
            result = crop_img(im)
            result.save(os.path.join(output_path,os.path.basename(img_path)))
def main(opts): 
    '''
    crop函数是需要传入一个元组作为参数
    靠改变n来实现
    '''
    input_path = opts.input_dirs
    output_path = opts.output_dirs
    load_img(input_path,output_path)
    print('finish!')
if __name__=='__main__':

    parser = ArgumentParser()
    parser.add_argument('--input_dirs',default='./input_img',help='path/to/your/input_img')
    parser.add_argument('--output_dirs',default='./output_img',help='path/to/your/output_img')
    opts = parser.parse_args()
    main(opts)