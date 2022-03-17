% faceply = pcread('BOX-ptcloud.ply');
facelands = textread('36faceland.txt');
xmin = min(facelands(:,1));
xmax = max(facelands(:,1));
ymin = min(facelands(:,2));
ymax = max(facelands(:,2));
facepoint1 = ptcloud36.Location;
facepoint = reshape(facepoint1,[],3);
colorpoint1 = ptcloud36.Color;
colorpoint = reshape(colorpoint1,[],3);
newfacepoint = [];
newcolorpoint = [];

% X:-0.07-0.15,Y:-0.15-0.07
% 34 if facepoint(i,1)>xmin+0.01 && facepoint(i,1)<xmax+0.04 && facepoint(i,2)>ymin && facepoint(i,2)<ymax+0.02
% 36 
for i=1:296758
   if facepoint(i,1)>xmin-0.02 && facepoint(i,1)<xmax-0.085 && facepoint(i,2)>ymin+0.04 && facepoint(i,2)<ymax+0.02
        newfacepoint = [newfacepoint facepoint(i,:)];
        newcolorpoint = [newcolorpoint colorpoint(i,:)];
   end 
end
newfacepoint = (reshape(newfacepoint,3,[]).');
newcolorpoint = (reshape(newcolorpoint,3,[]).');
fcpoint36 = pointCloud(newfacepoint,'Color',newcolorpoint);
pcshow(fcpoint36);
pcwrite(fcpoint36,'faceCutPoint36','PLYFormat','binary');