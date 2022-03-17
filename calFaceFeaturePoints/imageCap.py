import cv2

capLeft = cv2.VideoCapture(1)
capRight = cv2.VideoCapture(0)
# capLeft.set(3,960)
# capLeft.set(4,720)
# capRight.set(3,960)
# capRight.set(4,720)
i = 0
while True:
    sucessR , imgR = capRight.read()
    sucessL , imgL = capLeft.read()
    if  sucessL and sucessR:
        cv2.imshow('cameraRight', imgR)
        cv2.imshow('cameraLeft', imgL)
        k = cv2.waitKey(1)
        if k == 27:  # 通过esc键退出摄像
            break
        elif k == ord('s'):
            cv2.imwrite('D:/MyFiles/Pictures/20220301/left/' + str(i) + '-L.png', imgL)
            cv2.imwrite('D:/MyFiles/Pictures/20220301/right/' + str(i) + '-R.png', imgR)
            print("第%s张图片保存成功" % (i + 1))
            i += 1
    else:
        print('sucessL',sucessL)
        print('sucessR',sucessR)
        print('摄像头没插好，请重新插一遍')
        break
capRight.release()
capLeft.release()
cv2.destroyAllWindows()
# cv2.stereoRectify() 得到进行立体校正所需的映射矩阵
# cv2.stereoCalibrate()