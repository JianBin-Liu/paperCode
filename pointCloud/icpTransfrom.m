facepoint34 = pcread('faceCutPoint34.ply');
facepoint36 = pcread('faceCutPoint36.ply');
trans = pcregistericp(facepoint34,facepoint36);
fptran = pctransform(facepoint34,trans);
% figure;pcshowpair(facepoint34,facepoint36);
% figure;pcshowpair(fptran,facepoint36);
% mergepoint = pcmerge(fptran,facepoint36,10);
% figure;pcshow(mergepoint);
keypoints1 = zeros(68,3);
keypoints2 = zeros(68,3);
% transpoint34
for i=1:68 
    for j = 1:14678
        if fptran.Color(j,1)==i && fptran.Color(j,2)==0 && fptran.Color(j,3) ==255
            keypoints1(i,1) = fptran.Location(j,1);
            keypoints1(i,2) = fptran.Location(j,2);
            keypoints1(i,3) = fptran.Location(j,3);
        end
    end
end
% facepoint36
for i=1:68 
    for j = 1:14882
        if facepoint36.Color(j,1)==i && facepoint36.Color(j,2)==0 && facepoint36.Color(j,3) ==255
            keypoints2(i,1) = facepoint36.Location(j,1);
            keypoints2(i,2) = facepoint36.Location(j,2);
            keypoints2(i,3) = facepoint36.Location(j,3);
        end
    end
end

% fptranpoint = fptran.Location;
% fptranColor = fptran.Color;
% fptranpoint(:,1) = fptranpoint(:,1) + 0.0568;
% fptcloud = pointCloud(fptranpoint,'Color',fptranColor);
% fpoint36 =facepoint36.Location;
% fpColor36 = facepoint36.Color;
    % fptranpoint_36 = [fptranpoint;fpoint36];fptranColor_36 = [fptranColor;fpColor36];
    % tranpoint = pointCloud(fptranpoint_36,'Color',fptranColor_36);
    % figure;pcshow(tranpoint);
% trans2 = pcregistericp(fptcloud,facepoint36);
% fptcloud2 = pctransform(fptcloud,trans2);
% 
% fptcloud2vert = fptcloud2.Location;
% fptcloud2Col = fptcloud2.Color;
% allvert = [fptcloud2vert;fpoint36];
% allcolor = [fptcloud2Col;fpColor36];
% allpoint = pointCloud(allvert,'Color',allcolor);
% figure;pcshow(allpoint);

color1 = zeros(length(keypoints1),3);
color2 = zeros(length(keypoints2),3);
for i = 1:length(keypoints1)
    color1(i,1) = i;
    color1(i,2) = 0;
    color1(i,3) = 255;
    color2(i,1) = i;
    color2(i,2) = 0;
    color2(i,3) = 255;
end
a = [8 13 15 27 62 63 64];
keypoints1(a,:) = [];
keypoints2(a,:) = [];
color1(a,:) = [];
color2(a,:) = [];
pt1 = pointCloud(keypoints1,'Color',color1);
pt2 = pointCloud(keypoints2,'Color',color2);
figure;pcshowpair(pt2,pt1);
keytran = pcregistericp(pt2,pt1);
pt2_2 = pctransform(pt2,keytran);
figure;pcshowpair(pt2_2,pt1);
x_shift = sum(pt1.Location(:,1)-pt2_2.Location(:,1))/length(pt1.Location);
% y_shift = sum(pt1.Location(:,2)-pt2_2.Location(:,2))/length(pt1.Location);
verpt2_2 = pt2_2.Location;
colpt2_2 = pt2_2.Color;
verpt2_2(:,1) = verpt2_2(:,1) + x_shift;
pt2_2shift = pointCloud(verpt2_2,'Color',colpt2_2);
figure;pcshowpair(pt2_2shift,pt1);

