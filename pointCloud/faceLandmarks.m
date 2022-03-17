color = face34.Color;
point = face34.Location;
landpoints34 = zeros(68,3);
for count=1:68
   for i=1:14687
       if color(i,1)==count && color(i,2)==0 && color(i,3)==255
           landpoints34(count,1) = point(i,1);
           landpoints34(count,2) = point(i,2);
           landpoints34(count,3) = point(i,3);
       end
    end 
end
% f1 = fopen('34faceland.txt','w');
% fprintf(f1,'%.5f %.5f %.5f\n',landpoints.');
% fclose(f1);

% fepoint = (reshape(model.shapeMU,3,53215)).';
% modelpoints = zeros(68,3);
% for i = 1:68
%     modelpoints(i,1) = fepoint(model.kpt_ind(1,i),1);
%     modelpoints(i,2) = fepoint(model.kpt_ind(1,i),2);
%     modelpoints(i,3) = fepoint(model.kpt_ind(1,i),3);
% end
% f2 = fopen('modelland.txt','w');
% fprintf(f2,'%d %d %d\n',modelpoints.');
% fclose(f2);



