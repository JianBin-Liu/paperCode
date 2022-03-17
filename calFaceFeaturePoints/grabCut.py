import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('D:/MyFiles/Pictures/20220301/left/76-L-rect.png')
OLD_IMG = img.copy()
mask = np.zeros(img.shape[:2], np.uint8)
SIZE = (1, 65)
bgdModle = np.zeros(SIZE, np.float64)
fgdModle = np.zeros(SIZE, np.float64)
print(img.shape[1])
print(img.shape[0])
#rect = (1, 1, img.shape[1], img.shape[0])
rect = (240, 1, 220, 237)
# rect = (270, 0, 210, 210) #89
# rect(x,y,w,h)
cv2.grabCut(img, mask, rect, bgdModle, fgdModle, 10, cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img *= mask2[:, :, np.newaxis]


cv2.imwrite('D:/MyFiles/Pictures/20220301/left/76-L-rect-PY-cut.png', img)

plt.subplot(121), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("grabcut"), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(cv2.cvtColor(OLD_IMG, cv2.COLOR_BGR2RGB))
plt.title("original"), plt.xticks([]), plt.yticks([])

plt.show()