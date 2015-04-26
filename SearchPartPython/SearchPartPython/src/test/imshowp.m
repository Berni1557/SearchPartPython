function imshowp(I)
    Id=ones(size(I));
    Id(:,:,1)=I(:,:,3);
    Id(:,:,3)=I(:,:,1);
    Id(:,:,2)=I(:,:,2);
    I=uint8(Id);
    imshow(I)
end
