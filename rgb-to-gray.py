import cv2
import numpy 

img = cv2.imread("fuji.png")
print(type(img))
bitmap = img.copy()

#average weights 
R = 76.245
G = 149.685
B = 29.071

#converts original RGB image into gray-scale using avg weights 
row, col, _ = img.shape
for i in range(row):
    for j in range(col):
        b = img[i][j][0]*B
        g = img[i][j][1]*G
        r = img[i][j][2]*R
        bitmap[i][j]  = (r+b+g)/255

#display original RGB img and new gray-scale img
cv2.imshow("original",img)
cv2.imshow("gray",bitmap)
cv2.waitKey(0)
