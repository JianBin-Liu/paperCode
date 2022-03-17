img1 = imread('D:\MyFiles\Pictures\20220301\left\76-L.png');
img2 = imread('D:\MyFiles\Pictures\20220301\right\76-R.png');
% 76 88-112；89 96-120

[rectimg1,rectimg2] = rectifyStereoImages(img1,img2,stereoParams);
% imwrite(rectimg1,'D:\MyFiles\Pictures\20220301\left\89-L-rect.png');

rectimgCut1L76 = imread('D:\MyFiles\Pictures\20220301\left\76-L-rect-PY-cut.png');

grayrectimg1 = rgb2gray(rectimg1);
grayrectimg2 = rgb2gray(rectimg2); 

disparityRange = [88 112];

dispimgL = disparitySGM(grayrectimg1,grayrectimg2,'DisparityRange',disparityRange,'UniquenessThreshold',0);
% dispimgR = disparitySGM(grayrectimg2,grayrectimg1,'DisparityRange',disparityRange,'UniquenessThreshold',0);
figure;imshow(dispimgL, disparityRange);

meddispimgL = medfilt2(dispimgL,[3 3]); 
figure;imshow(meddispimgL,disparityRange);
% colormap jet;colorbar;

oricloud = reconstructScene(meddispimgL,stereoParams);
oricloud1 = double(oricloud) ./ 1000;
ptcloudL76 = pointCloud(oricloud1,'Color',rectimgCut1L76);
figure;pcshow(ptcloudL76);



