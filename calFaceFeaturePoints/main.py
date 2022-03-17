import cv2
import numpy as np
import matplotlib.pyplot as plt  # plt 用于显示图片
import matplotlib.image as mpimg  # mpimg 用于读取图片

# 预处理
from TFile.cameraRectify0813.shuangmu import StereoCalibration
from TFile.cameraRectify0813.stereoCameral import stereoCameral

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def preprocess(img1, img2):
    # 彩色图->灰度图
    im1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    im2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 直方图均衡
    im1 = cv2.equalizeHist(im1)
    im2 = cv2.equalizeHist(im2)

    return im1, im2


# 消除畸变
def undistortion(image, camera_matrix, dist_coeff):
    undistortion_image = cv2.undistort(image, camera_matrix, dist_coeff)

    return undistortion_image


# 获取畸变校正和立体校正的映射变换矩阵、重投影矩阵
# @param：config是一个类，存储着双目标定的参数:config = stereoconfig.stereoCamera()

def getRectifyTransform(height, width, config):
    # 读取内参和外参
    left_K = config.cam_matrix_left
    right_K = config.cam_matrix_right
    left_distortion = config.distortion_l
    right_distortion = config.distortion_r
    R = config.R
    T = config.T

    # 计算校正变换
    height = int(height)
    width = int(width)
    # P1 2 是新的相机内参矩阵, 双目下计算无畸变新相机内参矩阵
    R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(left_K, left_distortion, right_K, right_distortion,
                                                      (width, height), R, T, alpha=-1)
    #P 3*4投影矩阵 Q 4*4视差深度映射矩阵 计算无畸变和修正变换关系 返回映射关系矩阵
    # initUndistortRectifyMap对应参数 相机内参，畸变系数，旋转矩阵,新的相机内参，大小，m1type,map1,map2
    # cv2.initUndistortRectifyMap()
    map1x, map1y = cv2.initUndistortRectifyMap(left_K, left_distortion, R1, P1, (width, height), cv2.CV_16SC2)
    map2x, map2y = cv2.initUndistortRectifyMap(right_K, right_distortion, R2, P2, (width, height), cv2.CV_16SC2)
    # print('map1x,map1y',np.shape(map1x),np.shape(map1y))
    # print('map2x,map2y',np.shape(map2x),np.shape(map2y))
    return map1x, map1y, map2x, map2y, Q, roi1, roi2


# 畸变校正和立体校正
def rectifyImage(image1, image2, map1x, map1y, map2x, map2y):
    rectifyed_img1 = cv2.remap(image1, map1x, map1y, cv2.INTER_LINEAR)
    rectifyed_img2 = cv2.remap(image2, map2x, map2y, cv2.INTER_LINEAR)

    return rectifyed_img1, rectifyed_img2


# 立体校正检验----画线
def draw_line1(image1, image2):
    # 建立输出图像
    height = max(image1.shape[0], image2.shape[0])
    width = image1.shape[1] + image2.shape[1]

    output = np.zeros((height, width, 3), dtype=np.uint8)
    output[0:image1.shape[0], 0:image1.shape[1]] = image1
    output[0:image2.shape[0], image1.shape[1]:] = image2

    for k in range(15):
        cv2.line(output, (0, 50 * (k + 1)), (2 * width, 50 * (k + 1)), (0, 255, 0), thickness=1,
                 lineType=cv2.LINE_AA)  # 直线间隔：100

    return output


# 立体校正检验----画线
def draw_line2(image1, image2):
    # 建立输出图像
    height = max(image1.shape[0], image2.shape[0])
    width = image1.shape[1] + image2.shape[1]

    output = np.zeros((height, width), dtype=np.uint8)
    output[0:image1.shape[0], 0:image1.shape[1]] = image1
    output[0:image2.shape[0], image1.shape[1]:] = image2

    # for k in range(15):
    #     cv2.line(output, (0, 50 * (k + 1)), (2 * width, 50 * (k + 1)), (0, 255, 0), thickness=1,
    #              lineType=cv2.LINE_AA)  # 直线间隔：100

    return output


# 视差计算
def disparity_SGBM(left_image, right_image, down_scale=False):
    # SGBM匹配参数设置
    if left_image.ndim == 2:
        img_channels = 1
    else:
        img_channels = 3
    blockSize = 5
    # mindisp 起始搜索视差 numdisp搜索视差范围
    param = {'minDisparity': 64, 'numDisparities': 64, 'blockSize': blockSize, 'P1': 8 * img_channels * blockSize ** 2,
             'P2': 32 * img_channels * blockSize ** 2, 'disp12MaxDiff': 5, 'preFilterCap': 1, 'uniquenessRatio': 5,
             'speckleWindowSize': 50, 'speckleRange': 2, 'mode': cv2.STEREO_SGBM_MODE_SGBM}
    # 构建SGBM对象 单星号-将参数以元组形式导入，双星号-字典形式导入
    sgbm = cv2.StereoSGBM_create(**param)
    # 计算视差图
    size = (left_image.shape[1], left_image.shape[0])
    if down_scale == False:
        disparity_left = sgbm.compute(left_image, right_image)
        disparity_right = sgbm.compute(right_image, left_image)
    else:
        left_image_down = cv2.pyrDown(left_image)
        right_image_down = cv2.pyrDown(right_image)

        factor = size[0] / left_image_down.shape[1]
        disparity_left_half = sgbm.compute(left_image_down, right_image_down)
        disparity_right_half = sgbm.compute(right_image_down, left_image_down)
        disparity_left = cv2.resize(disparity_left_half, size, interpolation=cv2.INTER_AREA)
        disparity_right = cv2.resize(disparity_right_half, size, interpolation=cv2.INTER_AREA)
        disparity_left *= int(factor)
        disparity_right *= int(factor)
    # disparity_left = cv2.normalize(src=disparity_left, dst=disparity_left, beta=0, alpha=255,
    #                          norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    # disparity_right = cv2.normalize(src=disparity_right, dst=disparity_left, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX,
    #                                dtype=cv2.CV_8U)
    disparity_left = np.divide(disparity_left.astype(np.float32), 16.)
    disparity_right = np.divide(disparity_right.astype(np.float32), 16.)

    return disparity_left, disparity_right

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1,3)
    colors = colors.reshape(-1,3)
    verts = np.hstack([verts, colors])
    with open(fn, 'w') as f:
        f.write(ply_header % dict(vert_num=len(verts)))
        np.savetxt(f, verts, '%f %f %f %d %d %d')

if __name__ == '__main__':
    imgL0 = cv2.imread("D:/MyFiles/Pictures/imageCap/im2.png")
    imgR0 = cv2.imread("D:/MyFiles/Pictures/imageCap/im6.png")
    imgL1 = cv2.cvtColor(imgL0,cv2.COLOR_BGR2RGB)
    imgR1 = cv2.cvtColor(imgR0,cv2.COLOR_BGR2RGB)
    # imgL , imgR = preprocess(imgL ,imgR )
    biaoding = StereoCalibration()
    biaoding.calibration_photo()
    height, width = imgL1.shape[0:2]
    config = stereoCameral()  # 读取相机参数
    # 去畸变
    imgL = undistortion(imgL1, config.cam_matrix_left, config.distortion_l)
    imgR = undistortion(imgR1, config.cam_matrix_right, config.distortion_r)

    # 几何极线校正
    map1x, map1y, map2x, map2y, Q, roi1, roi2 = getRectifyTransform(height, width, config)
    print('Q:',Q)
    iml_rectified, imr_rectified = rectifyImage(imgL, imgR, map1x, map1y, map2x, map2y)
    # iml_rectified = cv2.flip(iml_rectified,-1)
    # imr_rectified = cv2.flip(imr_rectified,-1)
    # linepic = draw_line1(iml_rectified, imr_rectified)
    # 计算视差
    lookdispL, lookdispR = disparity_SGBM(iml_rectified, imr_rectified,down_scale=False)
    # newlookL = cv2.normalize(lookdispL,lookdispL,alpha=0,beta=255,norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_8U)
    bil_lookdispL = cv2.bilateralFilter(lookdispL,10,120,120)
    plt.figure();plt.imshow(bil_lookdispL,cmap='gray');plt.title('bilateral')
    # linepic2 = draw_line2(lookdispL, lookdispR)
    plt.figure();plt.imshow(lookdispL,cmap='gray');plt.title('lookdis')
    # plt.figure();plt.imshow(lookdispR)
    # 点云生成
    Q1 = [[1.00000000e+00, 0.00000000e+00, 0.00000000e+00, - 3.31945789e+02],
          [0.00000000e+00, -1.00000000e+00, 0.00000000e+00, 2.55202299e+02],
          [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, -6.19993572e+02],
          [0.00000000e+00, 0.00000000e+00, 1.45458382e-02, - 0.00000000e+00]]
    Q1 = np.array(Q1)
    # （透视/重）投影矩阵Q 可以通过stereoRectify
    print(lookdispL[100][100])
    pointsL = cv2.reprojectImageTo3D(lookdispL,Q)

    # pointsR = cv2.reprojectImageTo3D(lookdispR,Q)
    maskL = lookdispL > lookdispL.min()
    # maskR = lookdispR > lookdispR.min()
    outpointsL = pointsL[maskL]
    # outpointsR = pointsR[maskR]
    outcolorL = imgL1[maskL]
    # outcolorR = imgR1[maskR]
    write_ply('1028-1resultL.ply',outpointsL,outcolorL)
    print('save %s' % ('resultL.ply'))
    # write_ply('resultR.ply',pointsR,imgL1)
    # plt.figure();plt.imshow(linepic2)
    plt.show()
# points_3d = cv2.reprojectImageTo3D(lookdispL, Q)
# cv2.stereoRectifyUncalibrated()
# cv2.initUndistortRectifyMap()
