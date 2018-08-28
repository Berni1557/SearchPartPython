import cv2
from scipy.misc import imresize
from RegionGrowing import RegionGrowing

img_name = "gnu.jpg"
img = cv2.imread(img_name)
image_small = imresize(img, 0.5)

threshold = 10
reg_size_min=100
show = True
scale = 0.2

RG = RegionGrowing(threshold, reg_size_min, show, scale);
regions, regionsMap = RG.region_growing(image_small);

RG.drawContours(regions)

##########################################

cv2.namedWindow("regionsMap", cv2.WINDOW_NORMAL)
cv2.imshow('regionsMap', regionsMap) 
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('cont_out.png', regionsMap)



