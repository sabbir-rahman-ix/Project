import numpy as np

values = [5, 10, 15, 20, 25]
arr = np.array(values)

mean_value = np.mean(arr)
std_value = np.std(arr)
min_value = np.min(arr)
max_value = np.max(arr)

print("Array:", arr)
print("Mean:", mean_value)
print("Standard Deviation:", std_value)
print("Minimum:", min_value)
print("Maximum:", max_value)


import cv2
image = cv2.imread("hands.jpg", 0)


brightness = np.mean(image)
contrast = np.std(image)

print("Brightness:", brightness)
print("Contrast:", contrast)
