import cv2

# this loads the image from the disk
image = cv2.imread("images/study.jpg")

# To extract the height and width of the image
h, w = image.shape[:2]
# print(f"{h}, {w}")


# To extract the RGB values of the pixel at location (100, 100)
(b, g, r) = image[100, 100]
# print(f"{b}, {g}, {r}")
# to pass the channel to extract RGB values
B = image[100, 100][0]
# print(B)


# to extract the ROI
roi = image[100:500, 200:700]

# to resize the image
resized = cv2.resize(
    image, (800, 800)
)  # in this approach the ascpect ratio is not maintained and the image is distorted because of the different height and width


# to resize the image while maintaining the aspect ratio, we use the following approach
r = 800.0 / w

dim = (800, int(h * r))
resized = cv2.resize(image, dim)
# to rotate the image, we get its center, the rotation matric and then apply the warpAffine function or affine transformation
center = (w // 2, h // 2)
matrix = cv2.getRotationMatrix2D(center, -45, 1.0)
rotated = cv2.warpAffine(image, matrix, (w, h))
# to draw a rectangle in opencv, we use the rectangle function

output = image.copy()
cv2.rectangle(output, (100, 100), (200, 200), (0, 0, 255), 2)

# to write words on the image, we use the putText function
text = cv2.putText(
    output,
    "OpenCV + Jurassic Park!!!",
    (500, 550),
    cv2.FONT_HERSHEY_SIMPLEX,
    4,
    (255, 0, 0),
    2,
)
