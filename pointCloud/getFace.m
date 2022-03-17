hland = [];
hcolor = [];

for i=1:403
    for j=1:615
        if ptcloudL76.Color(i,j,1)~=0 && ptcloudL76.Color(i,j,2)~=0 && ptcloudL76.Color(i,j,3)~=0
            hland = [hland -ptcloudL76.Location(i,j,:)];
            hcolor = [hcolor ptcloudL76.Color(i,j,:)];
        end
    end
end

new_hptcloud76 = pointCloud(hland, 'Color', hcolor);
pcshow(new_hptcloud76);
