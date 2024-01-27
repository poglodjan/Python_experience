import numpy as np
import cv2 

img1= cv2.imread("astronom.png")
img2= cv2.imread("zadanie_6.01.png")

print(img1.shape)
print(img2.shape)

width, height = 183 , 275
img2=cv2.resize(img2, (width,height))

combined=np.hstack((img1,img2))
cv2.imshow("combined images", combined)
cv2.waitKey()
cv2.destroyAllWindows()

