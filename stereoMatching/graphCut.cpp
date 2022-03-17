#include "stdafx.h"
#include "opencv2/highgui/highgui.hpp"                                                                                               
#include "opencv2/imgproc/imgproc.hpp"
#include <ctime>
#include <iostream>

using namespace std;
using namespace cv;

string filename;
Mat image;
string winName = "show";
enum { NOT_SET = 0, IN_PROCESS = 1, SET = 2 };
uchar rectState;
Rect rect;
Mat mask;
const Scalar GREEN = Scalar(0, 255, 0);
Mat bgdModel, fgdModel;

void setRectInMask() {
	rect.x = max(0, rect.x);
	rect.y = max(0, rect.y);
	rect.width = min(rect.width, image.cols - rect.x);
	rect.height = min(rect.height, image.rows - rect.y);

}

static void getBinMask(const Mat& comMask, Mat& binMask) {
	binMask.create(comMask.size(), CV_8UC1);
	binMask = comMask & 1;
}

void on_mouse(int event, int x, int y, int flags, void*)
{
	Mat res;
	Mat binMask;

	switch (event) {
	case CV_EVENT_LBUTTONDOWN:
		if (rectState == NOT_SET) {
			rectState = IN_PROCESS;
			rect = Rect(x, y, 1, 1);
		}
		break;
	case CV_EVENT_LBUTTONUP:
		if (rectState == IN_PROCESS) {
			rect = Rect(Point(rect.x, rect.y), Point(x, y));
			rectState = SET;
			(mask(rect)).setTo(Scalar(GC_PR_FGD));
			image = imread(filename, 1);
			grabCut(image, mask, rect, bgdModel, fgdModel, 1, GC_INIT_WITH_RECT);
			getBinMask(mask, binMask);
			image.copyTo(res, binMask);
			imshow("11", res);
		}
		break;
	case CV_EVENT_MOUSEMOVE:
		if (rectState == IN_PROCESS) {
			rect = Rect(Point(rect.x, rect.y), Point(x, y));
			image = imread(filename, 1);
			rectangle(image, Point(rect.x, rect.y), Point(rect.x + rect.width, rect.y + rect.height), GREEN, 2);
			imshow(winName, image);
		}
		break;
	}
	std::vector<int> compression_params;
	compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
	compression_params.push_back(0);// 无压缩png.
	compression_params.push_back(cv::IMWRITE_PNG_STRATEGY);
	compression_params.push_back(cv::IMWRITE_PNG_STRATEGY_DEFAULT);
	imwrite("D:/MyFiles/Pictures/20220301/left/89-L-rect-cut.png", res);
}

int main(int argc, char* argv[]) {

	filename = "D:/MyFiles/Pictures/20220301/left/89-L-rect.png";
	//filename = "D:/MyFiles/Pictures/0327-2/right/new1-R-rect.png";
	image = imread(filename, 1);
	imshow(winName, image);
	mask.create(image.size(), CV_8UC1);
	rectState = NOT_SET;
	mask.setTo(GC_BGD);

	setMouseCallback(winName, on_mouse, 0);
	waitKey(0);

	//const int max_row = 2000;
	//const int max_col = 2000;
	//int(*a)[max_col] = new int[max_row][max_col];
	//clock_t start, finish;

	//
	////先列后行
	//start = clock();
	//for (int i = 0; i<max_col; i++)
	//	for (int j = 0; j<max_row; j++)
	//		a[j][i] = 1;
	//finish = clock();
	////totaltime=(double)()/clocks_per_sec;
	//cout << "先列后行遍历时间为：" << finish - start << "ms" << endl;
	////先行后列
	//start = clock();
	//for (int i = 0; i<max_row; i++)
	//	for (int j = 0; j<max_col; j++)
	//		a[i][j] = 1;
	//finish = clock();
	////totaltime=(double)()/clocks_per_sec;
	//cout << "先行后列遍历时间为：" << finish - start << "ms" << endl;
	//return 0;
}