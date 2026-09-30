import cv2

# ছবি লোড করা
img = cv2.imread("C:/Users/USER/OneDrive/Desktop/Proejct/computer vision/hands.jpg")

# সাইজ ছোট করা
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

# ছবির সাইজ বা শেপ প্রিন্ট করা
h, w, c = img.shape
print("Height:", h)
print("Width:", w)
print("Channels:", c)

# ছবিকে গ্রে-স্কেল বা কালো-সাদায় রূপান্তর করা
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# আউটপুট স্ক্রিনে ছবি দেখানো
cv2.imshow("My Hand Image", gray_img)

# কী-বোর্ডে কোনো বাটন চাপলে উইন্ডো বন্ধ হবে
cv2.waitKey(0)
cv2.destroyAllWindows()