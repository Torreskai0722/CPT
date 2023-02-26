import numpy as np
from PIL import Image 
from scipy.signal import convolve2d
import glob
import os
import cv2

def image_paths():
    VIDEO_FILE = '/home/mobilitylab/images/'

    # a = ['cac07407-0396e053', 'cac07407-196cd6f8', 'cac07407-951977c8', 'cac07407-0eb1c8bf', 
    # 'cac07407-ba37148a', 'cac07407-e969f06a', 'cac07407-bc0b048a', 'cac07407-15b814db', 
    # 'cac07407-76e4c968', 'cac07407-fe32e494']
    
    # a = ['cac07407-0396e053', 'cac07407-196cd6f8', 'cac07407-951977c8', 'cac07407-0eb1c8bf']

    a = ['cac07407-0396e053']

    paths = []
    for i in a:
        # print(i)
        pd = glob.glob(os.path.join(VIDEO_FILE + str(i) + "/", '*.jpg'))
        paths.extend(pd)
    paths = sorted(paths, key=os.path.getmtime)
    print(len(paths))

    return paths
 
def matlab_style_gauss2D(shape=(3,3),sigma=0.5):
    #高斯加窗
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h
 
def filter2(x, kernel, mode='same'):
    #窗口内进行高斯卷积，类似加权平均
    return convolve2d(x, np.rot90(kernel, 2), mode=mode)
 
def compute_ssim(im1, im2, k1=0.01, k2=0.03, win_size=11, L=255):
    M, N = im1.shape
    C1 = (k1*L)**2
    C2 = (k2*L)**2
    window = matlab_style_gauss2D(shape=(win_size,win_size), sigma=1.5)
    window = window/np.sum(np.sum(window))
 
    if im1.dtype == np.uint8:
        im1 = np.double(im1)
    if im2.dtype == np.uint8:
        im2 = np.double(im2)
 
    mu1 = filter2(im1, window, 'valid')
    mu2 = filter2(im2, window, 'valid')
    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = filter2(im1*im1, window, 'valid') - mu1_sq
    sigma2_sq = filter2(im2*im2, window, 'valid') - mu2_sq
    sigmal2 = filter2(im1*im2, window, 'valid') - mu1_mu2
 
    ssim_map = ((2*mu1_mu2+C1) * (2*sigmal2+C2)) / ((mu1_sq+mu2_sq+C1) * (sigma1_sq+sigma2_sq+C2))
 
    return np.mean(np.mean(ssim_map))

def ssim(former_img, img):
    former_img = Image.fromarray(former_img)
    img = Image.fromarray(img)
    return compute_ssim(np.array(former_img.resize((8, 8), Image.ANTIALIAS).convert('L'), 'f'),np.array(img.resize((8, 8), Image.ANTIALIAS).convert('L'), 'f'))
 
if __name__ == "__main__":
    # image1 = Image.open('image1.jpeg')
    # image2 = Image.open('image2.jpeg')
    # f = open('ssim-residential-10.log','wt')
    paths = image_paths()
    former_img = Image.open(paths[0])
    #former_img_resize = np.array(former_img.resize((25, 25), Image.ANTIALIAS).convert('L'), 'f')
    #print(former_img.size)
    #print(former_img_resize)
    
    # step = 400
    for step in range(100):
        f = open('./ssim-logs-new/ssim-step_'+str(step)+'.log','wt')
        for count, path in enumerate(paths):
            if count >= step:
                img = Image.open(path)
                former_img = Image.open(paths[count-step])
                s = compute_ssim(np.array(former_img.resize((25, 25), Image.ANTIALIAS).convert('L'), 'f'),np.array(img.resize((25, 25), Image.ANTIALIAS).convert('L'), 'f'))
                f.write(str(s)+'\n')
        f.close()