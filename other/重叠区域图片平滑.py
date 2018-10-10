import numpy as np
from PIL import Image


def default_loader(path):
    return Image.open(path)


def optimize_seam_with_smooth(first, second, lr_or_up=True):
    """优化图片拼接边缘
    平滑过渡重叠区域，动态设置重叠区域 alpha 平滑参数
    :param first: PIL （left or up image）
    :param second: PIL (right or down image)
    :param lr_or_up: bool (default True: left-right , False: up-down)
    :return: PIL 融合之后的图片（平滑边界）
    """
    assert first.size == second.size  # same size
    w, h = first.size  # 获取size
    im_arr_1st = np.asarray(first)  # PIL to ndarray
    im_arr_2nd = np.asarray(second)

    if lr_or_up:  # left-right
        alpha_arr = np.ones((h, w, 3))
        left = first.load()  # left image
        for i in range(w):
            for j in range(h):
                if sum(left[i, j]) > 0.1:  # 当前位置像素rgb值均不为0
                    alpha_arr[j, i, :] = (w - i) / w
        im_arr = im_arr_1st * alpha_arr + im_arr_2nd * (1 - alpha_arr)
    else:  # up-down
        alpha_arr = np.ones((h, w, 3))
        up = first.load()  # up image
        for i in range(w):
            for j in range(h):
                if sum(up[i, j]) > 0.1:
                    alpha_arr[j, i, :] = (h - j) / h
        im_arr = im_arr_1st * alpha_arr + im_arr_2nd * (1 - alpha_arr)  # 平滑计算
    return Image.fromarray(np.uint8(im_arr))
