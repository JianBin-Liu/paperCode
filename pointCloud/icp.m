%%kd-tree ��������
function [P_registered,e1,e2,R,T]=icp(P,Q,max_iterations)
tic
NS = createns(Q,'NSMethod','kdtree');
j=0;
d=100;
n=size(P,1);
R_final=eye(3,3);
while d>10e-30
    j=j+1;
    fprintf("����������%d\n",j);
    if j>max_iterations
        break
    end
    %Ѱ��Q�Ķ�Ӧ�㼯
    [idx, ~] = knnsearch(NS,P,'k',1);
    Qn= Q(idx,:);
    
    %������ת����R��ƽ�ƾ���t�����Ž⣬ʹ��svd����
    centerP=mean(P);    %P�㼯�����ĵ�
    centerQn=mean(Qn);      %��Ӧ�㼯�����ĵ�
    tempP=P-centerP;        %����ȥ���Ļ�
    tempQn=Qn-centerQn;
    
     H=tempP'*tempQn;  %�õ�H����
     [U,~,V]=svd(H);
     
     R=V*U';
    fprintf("��ת����\n");
    R_final=R*R_final
    %     T=(centerP-centerMap)';
    fprintf("ƽ�ƾ���\n");
    T=-R*centerP'+centerQn';  %�������ĵ����T����
 
    %ʹ��R��T���õ��µĵ㼯
    P=(R*P'+T)';       %ʹ��ת�������õ��µĵ㼯P
    d=sum(sum((P-Qn).^2,2))/n;	%�����µĵ㼯P����Ӧ���ƽ������
    e1=std(sum((P-Qn).^2,2));
    e2=d;
end
P_registered = P;
toc
