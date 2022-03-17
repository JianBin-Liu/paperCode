import cv2
import numpy as np

#读中文路径 假设 im_name是中文路径
#im = cv2.imdecode(np.fromfile(im_name,dtype=np.uint8),-1) # 读取的数据是RGB 而不是 BGR， 要注意

img1_rectified = cv2.imread('D:/Codes/PycharmProjects/3dRebuild/TFile/image/0-L.jpg')
img2_rectified = cv2.imread('D:/Codes/PycharmProjects/3dRebuild/TFile/image/0-R.jpg')
view1 = cv2.imread('D:/Codes/PycharmProjects/3dRebuild/TFile/image/view1.png')
view5 = cv2.imread('D:/Codes/PycharmProjects/3dRebuild/TFile/image/view5.png')
con1 = cv2.imread('D:/Codes/VS2019Projects/PatchMatchStereo-master/PatchMatchStereo-master/Data/Cone/im2.png')
con2 = cv2.imread('D:/Codes/VS2019Projects/PatchMatchStereo-master/PatchMatchStereo-master/Data/Cone/im6.png')
num = 5
blockSize = 13
# param = {'minDisparity': 0, 'numDisparities': 128, 'blockSize': blockSize, 'P1': 8 * img_channels * blockSize ** 2,
#              'P2': 32 * img_channels * blockSize ** 2, 'disp12MaxDiff': 1, 'preFilterCap': 63, 'uniquenessRatio': 15,
#              'speckleWindowSize': 100, 'speckleRange': 1, 'mode': cv2.STEREO_SGBM_MODE_SGBM_3WAY}
stereo_sgbm = cv2.StereoSGBM_create(minDisparity = 0, numDisparities = 64,blockSize = 5, P1 = 8 * 3 * blockSize * blockSize,
                                    P2 = 32 * 3 * blockSize * blockSize,disp12MaxDiff = 10, preFilterCap = 15,uniquenessRatio = 0,
                                    speckleWindowSize = 100,speckleRange = 2, mode = cv2.STEREO_SGBM_MODE_SGBM_3WAY)
# 新版opencv中没有ximgproc模块包(pip install opencv-contrib-python==3.4.2.16)
stereo_sgbm_right_matcher = cv2.ximgproc.createRightMatcher(stereo_sgbm)
# DisparityWLSFilter:基于加权最小二乘滤波的视差图滤波(以快速全局平滑的形式，比传统的加权最小二乘滤波实现快得多)，并可选地使用基于左右一致性的置信度来细化半遮挡和均匀区域的结果
wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=stereo_sgbm)
# Lambda是一个定义过滤期间正则化数量的参数。较大的值会迫使经过过滤的视差图边缘与源图像边缘粘连得更紧。典型值为8000。
wls_filter.setLambda(8000)
# SigmaColor定义了滤波过程对源图像边缘的敏感度。较大的值会通过低对比度边缘导致视差泄漏。较小的值会使过滤器对源图像中的噪声和纹理过于敏感。典型的值范围从0.8到2.0。
wls_filter.setSigmaColor(1.2)

# 将图片置为灰度图
gray_L = cv2.cvtColor(con1, cv2.COLOR_BGR2GRAY)
gray_R = cv2.cvtColor(con2, cv2.COLOR_BGR2GRAY)
# 计算视差: 根据SGBM方法生成差异图
disparity_left = stereo_sgbm.compute(gray_L, gray_R)
disparity_right = stereo_sgbm_right_matcher.compute(gray_R, gray_L)
cv2.imshow("before left",disparity_left)
cv2.imshow("before right",disparity_right)
disparity_left = np.int16(disparity_left)
disparity_right = np.int16(disparity_right)
cv2.imshow("after left",disparity_left)
cv2.imshow("after right",disparity_right)
# 视差图后处理
disparity_filtered = wls_filter.filter(disparity_left, gray_L, None, disparity_right)
cv2.imshow("disparity_filtered",disparity_filtered)
# 将图片扩展至3d空间中，其z方向的值则为当前的距离;
h, w = img1_rectified.shape[:2]
f = 0.8*w
Q = np.float32([[1, 0, 0, -0.5*w],
                    [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis,
                    [0, 0, 0,     -f], # so that y-axis looks up
                    [0, 0, 1,      0]])
# 通过reprojectImageTo3D这个函数将视差矩阵转换成实际的物理坐标矩阵,获取世界坐标
# threeD = cv2.reprojectImageTo3D(disparity_filtered.astype(np.float32) / 16.0, Q) * 2.8346
# threeD = cv2.reprojectImageTo3D(disparity_left.astype(np.float32) / 16.0, Q)*2.8346
# 获取深度图
disp_filtered = cv2.normalize(src=disparity_filtered, dst=disparity_filtered, alpha=255,beta = 0, norm_type = cv2.NORM_MINMAX)
disp_filtered = np.uint8(disp_filtered)
cv2.imshow("depth", disp_filtered)
cv2.waitKey(0)