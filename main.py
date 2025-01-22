
# Main code for trying out stuff and messing around
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def watershed_algorithm(image):
    # 边缘保留滤波EPF  去噪
    blur = cv.pyrMeanShiftFiltering(image,sp=10,sr=100)
    # 转成灰度图像
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    # 得到二值图像   自适应阈值
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

    # 形态学操作   获取结构元素  开操作
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    opening = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel=kernel, iterations=2)
    # 确定区域
    sure_bg = cv.dilate(opening, kernel, iterations=3)
    # cv.imshow('mor-opt', sure_bg)

    # 距离变换
    dist = cv.distanceTransform(opening, cv.DIST_L2, 3)
    dist_out = cv.normalize(dist, 0, 1.0, cv.NORM_MINMAX)
    # cv.imshow('distance-', dist_out * 50)
    ret, surface = cv.threshold(dist_out, dist_out.max() * 0.6, 255, cv.THRESH_BINARY)
    # cv.imshow('surface-markers', surface)

    surface_fg = np.uint8(surface)    # 转成8位整型
    unkonown = cv.subtract(sure_bg, surface_fg)        # 找到位置区域
    # Marker labelling
    ret, markers = cv.connectedComponents(surface_fg)  # 连通区域
    print(ret)

    # 分水岭变换
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    # Now, mark the region of unknown with zero
    markers[unkonown == 255] = 0
    markers[unkonown != 255] = 1
    plt.subplot(121)
    plt.imshow(markers)

    # 实施分水岭算法了。标签图像将会被修改，边界区域的标记将变为 -1
    markers = cv.watershed(image, markers=markers)
    image[markers == -1] = [0, 0, 255]      # 被标记的区域   设为红色
    plt.subplot(122)
    plt.imshow(image)


src = cv.imread(r'C:/Users/louis/OneDrive - The Hong Kong Polytechnic University/URIS/URIS Data/jats_incline_20250117/Shared Data/Static Data/Vegetation/skyview.jpg')
# src = cv.resize(src, None, fx=0.5, fy=0.5)
# plt.imshow(src)
watershed_algorithm(src)