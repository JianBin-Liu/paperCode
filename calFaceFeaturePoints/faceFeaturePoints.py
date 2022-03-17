import dlib
import numpy as np
import cv2
import matplotlib.pyplot as plt

def cha(img,flag):
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    img1 = img
    imggray = cv2.cvtColor(img1,cv2.COLOR_RGB2GRAY)
    faces = detector(imggray,0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if len(faces) !=0:
        for i in range(len(faces)):
            landmarks = np.array([[p.x,p.y] for p in predictor(img1,faces[i]).parts()])
            if flag:
                for idx, point in enumerate(landmarks):
                    pos = (point[0], point[1])
                    cv2.circle(img1, pos, 2, color=(0, 255, 0))
                    #cv2.putText(img1, str(idx + 1), pos, font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(img1, 'faces:' + str(len(faces)), (20, 50), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    else:
        landmarks=[]
        cv2.putText(img1,'no faces',(20,50),font,1,(0,0,0),1,cv2.LINE_AA)
    return img1,landmarks

if __name__ == '__main__':
    #new1-R-rect
    img1 = cv2.imread('D:/MyFiles/Pictures/20220301/left/76-L-rect.png') # 实际上是R图
    img2 = cv2.imread('D:/MyFiles/Pictures/20220301/right/76-R-rect.png') # L
    img11, land1 = cha(img1, True)
    img22, land2 = cha(img2, True)

    # x1 = min(land1[:, 0])
    # y1 = min(land1[:, 1])
    # w1 = max(land1[:, 0]) - min(land1[:, 0])
    # h1 = max(land1[:, 1]) - min(land1[:, 1])
    # print("89-x-y-w-h:", x1, y1, w1, h1)
    #
    # x2 = min(land2[:, 0])
    # y2 = min(land2[:, 1])
    # w2 = max(land2[:, 0]) - min(land2[:, 0])
    # h2 = max(land2[:, 1]) - min(land2[:, 1])
    # print("76-x-y-w-h:", x2, y2, w2, h2)

    # file_path = 'D:/Codes/PyCharmProjects/20211121/Two/image/'
    # img01 = cv2.imread(file_path+'gamma01.png')
    # img03 = cv2.imread(file_path+'gamma03.png')
    # img18 = cv2.imread(file_path+'gamma18.png')
    # img25 = cv2.imread(file_path+'gamma25.png')

    #img2 = cv2.imread('D:/MyFiles/Pictures/0327-2/right/new1-R-rect.png')
    # img_Ori, land = cha(img, True)
    # img11, land11 = cha(img01, True)
    # img33, land33 = cha(img03, True)
    # img188, land18 = cha(img18, True)
    # img255, land25 = cha(img25, True)

    # sum01x = 0
    # sum01y = 0
    #
    # sum03x = 0
    # sum03y = 0
    #
    # sum18x = 0
    # sum18y = 0
    #
    # sum25x = 0
    # sum25y = 0
    #
    # for i in range(0,68):
    #     sum01x += land11[i][0] - land[i][0]
    #     sum01y += land11[i][1] - land[i][1]
    #
    #     sum03x += land33[i][0] - land[i][0]
    #     sum03y += land33[i][1] - land[i][1]
    #
    #     sum18x += land18[i][0] - land[i][0]
    #     sum18y += land18[i][1] - land[i][1]
    #
    #     sum25x += land25[i][0] - land[i][0]
    #     sum25y += land25[i][1] - land[i][1]

    # print("gamma0.1")
    # print(sum01x, sum01x / 68)
    # print(sum01y, sum01y / 68)
    #
    # print("gamma0.3")
    # print(sum03x, sum03x / 68)
    # print(sum03y, sum03y / 68)
    #
    # print("gamma1.8")
    # print(sum18x, sum18x / 68)
    # print(sum18y, sum18y / 68)
    #
    # print("gamma2.5")
    # print(sum25x, sum25x / 68)
    # print(sum25y, sum25y / 68)
    #img22, land22 = cha(img2, True)

    # cv2.imshow('img', img_Ori)
    # cv2.imshow('img11',img11)
    # cv2.imshow('img33', img33)
    # cv2.imshow('img188', img188)
    # cv2.imshow('img255', img255)
    # cv2.waitKey(0)

    disp1 = []
    disp2 = []
    for i in range(68):
        disp1.append(land2[i, 0]-land1[i, 0])
        disp2.append(land1[i, 0]-land2[i, 0])
    print(max(disp1))
    print(min(disp1))
    print(max(disp1)+(8-(max(disp1) % 8)))
    print(min(disp1)-(min(disp1) % 8))
    print("--右减坐---")
    print(max(disp2))
    print(min(disp2))
    print(max(disp2) + (8 - (max(disp2) % 8)))
    print(min(disp2) - (min(disp2) % 8))

    # with open('D:/MyFiles/Pictures/0327-2/land-new1-R57.txt', 'w') as f:
    #     for i in range(17,68):
    #         f.write(str(land11[i, 0]))
    #         f.write(' ')
    #         f.write(str(land11[i, 1]))
    #         f.write('\n')
    # f.close()
    # with open('D:/MyFiles/Pictures/0327-2/land-new0-R57.txt', 'w') as f:
    #     for i in range(17,68):
    #         f.write(str(land22[i, 0]))
    #         f.write(' ')
    #         f.write(str(land22[i, 1]))
    #         f.write('\n')
    # f.close()
