#include "stdafx.h"
#include<iostream>
#include<math.h>
using namespace std;
int i, j;
double *res1;
double *res2;




double *rowsum(double table[4][4], int nrow)//定义第i行的边际概率函数
{
	double res[4];
	for (i = 0; i<nrow; i++)
	{
		double count = 0;
		for (j = 0; j<4; j++)
			count += table[i][j];
		res[i] = count;
	}
	return res;
}
double *liesum(double table[4][4], int nlie)//定义第j列的边际概率函数
{	
	double res[4];
	for (j = 0; j<nlie; j++)
	{
		double count = 0.0;
		for (i = 0; i < 4; i++)
			count += table[i][j];
		res[j] = count;
	}
	return res;
}
void rmain()
{
	double p[4][4] = { { 1.0 / 8.0,1.0 / 16.0,1.0 / 32.0,1.0 / 32.0 },{ 1.0 / 16.0,1.0 / 8.0,1.0 / 32.0,1.0 / 32.0 },
	{ 1.0 / 16.0,1.0 / 16.0,1.0 / 16.0,1.0 / 16.0 },{ 1.0 / 4.0,0.0,0.0,0.0 } };
	for (i = 0; i<4; i++)//输出概率矩阵
	{
		for (j = 0; j<4; j++)
			cout << p[i][j] << " ";
		cout << endl;
	}cout << endl;
	res1 = rowsum(p, 4);//调用函数输出第i行的边际概率 
	for (i = 0; i<4; i++)
	{
		cout << "第" << i << "行的边际概率p" << "[" << i << "]" << "是" << res1[i] << endl;
	}cout << endl;
	res2 = liesum(p, 4);//调用函数输出第j列的边际概率
	for (j = 0; j<4; j++)
	{
		cout << "第" << j << "列的条件概率p" << "[" << j << "]" << "是" << res2[j] << endl;
	}cout << endl;
	// double p[4][4];
	double H1 = 0.0;
	for (i = 0; i<4; i++)
	{
		H1 += res1[i] * (log((1.0 / res1[i]) / log(2.0)));
	}
	double H2 = 0.0;
	for (j = 0; j<4; j++)
	{
		H2 += res2[j] * (log((1.0 / res2[j]) / log(2.0)));
	}
	double H3 = 0.0;
	for (i = 0; i<4; i++)
		for (j = 0; j<4; j++)
		{
			H3 += p[i][j] * (log(1.0 / p[i][j]) / log(2.0));
		}
	cout << "X的熵：H(X)=" << H1 << endl;
	cout << "Y的熵：H(Y)=" << H2 << endl;
	cout << "(X,Y)的熵：H(X,Y)=" << H3 << endl;
	cout << endl;
	cout << "条件熵：H(X|Y)=" << H3 - H2 << endl;
	cout << "条件熵：H(Y|X)=" << H3 - H1 << endl;
	cout << "互信息：I(X;Y)=" << H1 + H2 - H3 << endl;
	//int size = 4;//定义联合概率p为维数组
	//double *p;
	//p = new double[size];
	//for (i = 0; i<4; i++)//联合概率计算
	//{
	//	for (j = 0; j<4; j++)
	//	{
			/*int nSize;
			scanf( "%d", &nSize );
			int *p = ( int* )malloc( sizeof( int ) * nSize );
			for( int i = 0; i < nSize; i++ )
			p[ i ] = 0;

			double table[4][4];
			p[i]=pp[0][i]*table[i][j];
			cout<<"联合概率"<<"p"<<"["<<i<<"]"<<"["<<j<<"]""是"<<p[i]<<endl;

			}
			}
			for ( i=0;i<4;i++)//联合熵的计算
			{
			for ( j=0;j<4;j++)
			{

			// H+=p[i][j]*log(1.0/p[i][j]);
			H+=p[i]*(log((1.0/p[i])/log(2.0)));
			}
			}
			cout<<"联合H(x,y)熵为"<<H<<endl;
			delete []p; */
		}