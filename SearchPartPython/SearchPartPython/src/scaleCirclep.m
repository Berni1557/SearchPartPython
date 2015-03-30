function [scale_factor]=scaleCirclep(I)

addpath(genpath('/home/bernifoellmer/Studium/Masterarbeit/Mastertheses_code')) 

Id=ones(size(I));
Id(:,:,1)=I(:,:,3);
Id(:,:,3)=I(:,:,1);
Id(:,:,2)=I(:,:,2);
I=uint8(Id);
    
sc=2000/size(I,2);
ecc=0.7;

% scale image
I1=imresize(I,sc);

% % rgb to hsv transform
% I_hsv = rgb2hsv(I1);
% 
% % select illumination channel
% IL=I_hsv(:,:,3);
% 
% %discrete cosin transform
% Id = dct2(IL);
% 
% % bandpass filter
% f1=1;
% %f2=1000;
% h=ones(size(Id));
% h(1:f1,1:f1)=zeros(f1);
% %h(f2:end,f2:end)=zeros(size(h,1)-f2+1,size(h,2)-f2+1);
% If = Id.*h;
% 
% % inverse cosin transform
% Iin = idct2(If);
% 
% % global otsu theshold
% level = graythresh(Iin);
% BW = ~im2bw(Iin, level);
BW = ~thresholdLocally(I1);

% closing operator
se = strel('rectangle',[5,5]);
BWc = imclose(BW,se);

% estimate blob properties Centroid, thresholdLocallyEccentricity, EulerNumber, BoundingBox
STATS = regionprops(BWc,'Centroid','Eccentricity','EulerNumber','BoundingBox');
Eccentricity = cat(1, STATS.Eccentricity);
Centroid = cat(1, STATS.Centroid);
BoundingBox = cat(1, STATS.BoundingBox);

% S = regionprops(BWc,'PixelIdxList');
% ind1=(Eccentricity<ecc);
% for i=1:size(S,1)
%     if(ind1(i)==0)
%         BWc(S(i).PixelIdxList)=0;
%     end
% end

% filter blobs by Eccentricity

BoundingBox=BoundingBox(Eccentricity<ecc,:);
Centroid=Centroid(Eccentricity<ecc,:);


% filter blobs by BoundingBox
diameter_min=25;
diameter_max=500;

% ind2=(BoundingBox(:,4)>diameter_min) .* (BoundingBox(:,4)<diameter_max) .* (BoundingBox(:,3)>diameter_min) .* (BoundingBox(:,3)<diameter_max);
% S = regionprops(BWc,'PixelIdxList');
% for i=1:size(S,1)
%     if(ind2(i)==0)
%         BWc(S(i).PixelIdxList)=0;
%     end
% end
% imshow(BWc);

ind=find((BoundingBox(:,4)>diameter_min) .* (BoundingBox(:,4)<diameter_max) .* (BoundingBox(:,3)>diameter_min) .* (BoundingBox(:,3)<diameter_max));
Centroid=Centroid(ind,:);
BoundingBox=BoundingBox(ind,:);



if(~isempty(ind))
    % distance between centroids
    D = pdist2(Centroid,Centroid);
    D=D+diag(ones(size(D,1),1)*100);
    [C,rowmaxarray]=min(D);
    [distvalue,b]=min(C);
    a=rowmaxarray(b);


    % check max distance
    distance_max=10;
    if(distvalue>distance_max)
        scale_factor=false;
    else
        % compute diameter for bigger black circle
        if(mean(BoundingBox(a,3:4))>mean(BoundingBox(b,3:4)))
            d = mean(BoundingBox(a,3:4))/sc;
        else
            d = mean(BoundingBox(b,3:4))/sc;
        end
        scale_factor=25.86*(d/198);
        %scale_factor=0.1465*d;
    end
else
    scale_factor=NaN;
end

end