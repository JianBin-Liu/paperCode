#include "stdafx.h"
#include<iostream>
#include<math.h>
using namespace std;
int i, j;
double *res1;
double *res2;




double *rowsum(double table[4][4], int nrow)//�����i�еı߼ʸ��ʺ���
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
double *liesum(double table[4][4], int nlie)//�����j�еı߼ʸ��ʺ���
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
	for (i = 0; i<4; i++)//������ʾ���
	{
		for (j = 0; j<4; j++)
			cout << p[i][j] << " ";
		cout << endl;
	}cout << endl;
	res1 = rowsum(p, 4);//���ú��������i�еı߼ʸ��� 
	for (i = 0; i<4; i++)
	{
		cout << "��" << i << "�еı߼ʸ���p" << "[" << i << "]" << "��" << res1[i] << endl;
	}cout << endl;
	res2 = liesum(p, 4);//���ú��������j�еı߼ʸ���
	for (j = 0; j<4; j++)
	{
		cout << "��" << j << "�е���������p" << "[" << j << "]" << "��" << res2[j] << endl;
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
	cout << "X���أ�H(X)=" << H1 << endl;
	cout << "Y���أ�H(Y)=" << H2 << endl;
	cout << "(X,Y)���أ�H(X,Y)=" << H3 << endl;
	cout << endl;
	cout << "�����أ�H(X|Y)=" << H3 - H2 << endl;
	cout << "�����أ�H(Y|X)=" << H3 - H1 << endl;
	cout << "����Ϣ��I(X;Y)=" << H1 + H2 - H3 << endl;
	//int size = 4;//�������ϸ���pΪά����
	//double *p;
	//p = new double[size];
	//for (i = 0; i<4; i++)//���ϸ��ʼ���
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
			cout<<"���ϸ���"<<"p"<<"["<<i<<"]"<<"["<<j<<"]""��"<<p[i]<<endl;

			}
			}
			for ( i=0;i<4;i++)//�����صļ���
			{
			for ( j=0;j<4;j++)
			{

			// H+=p[i][j]*log(1.0/p[i][j]);
			H+=p[i]*(log((1.0/p[i])/log(2.0)));
			}
			}
			cout<<"����H(x,y)��Ϊ"<<H<<endl;
			delete []p; */
		}