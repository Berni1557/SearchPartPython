function [s]=evalmat(func,I)

tic;
addpath(genpath('/home/bernifoellmer/Studium/Masterarbeit/Mastertheses_code')) 

Id=ones(size(I));
Id(:,:,1)=I(:,:,3);
Id(:,:,3)=I(:,:,1);
Id(:,:,2)=I(:,:,2);
I=uint8(Id);

[s] = feval(func, I);

end