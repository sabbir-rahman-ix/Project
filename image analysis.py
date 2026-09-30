import cv2

img = cv2.imread("hands.jpg")
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

height, width, channels = img.shape

print("height:", height)
print("width:", width)
print("channels:", channels)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("Gray Image", gray)
cv2.waitKey(0)
