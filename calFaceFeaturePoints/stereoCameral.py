import numpy as np
import cv2


# 双目相机参数
from TFile.cameraRectify0813.shuangmu import stereo

class stereoCameral(object):
    def __init__(self):
        # 左相机内参数
        self.cam_matrix_left = stereo.m1
        # 右相机内参数
        self.cam_matrix_right = stereo.m2

        # 左右相机畸变系数:[k1, k2, p1, p2, k3]
        self.distortion_l = stereo.d1
        self.distortion_r = stereo.d2
        # 旋转矩阵

        self.R = stereo.R
        # 平移矩阵
        self.T = stereo.T

        # self.baseline = stereo.T[0]
