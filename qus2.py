from scipy.spatial.distance import euclidean, cityblock, cosine

v1 = [3, 5, 9]
v2 = [6, -2, 1]

euclidean_distance = euclidean(v1, v2)
manhattan_distance = cityblock(v1, v2)
cosine_distance = cosine(v1, v2)

print("Euclidean Distance:", euclidean_distance)
print("Manhattan Distance:", manhattan_distance)
print("Cosine Distance:", cosine_distance)