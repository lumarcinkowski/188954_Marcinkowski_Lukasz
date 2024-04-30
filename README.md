This code uses the OpenCV library (cv2) and NumPy library (np). CV2 are used for only image loading.
1. Next we read two images, one edited (dublin_edited.jpg) and one original (dublin.jpg), using OpenCV's imread function. These images are stored in imgEdited and imgOriginal variables respectively.


imgOryginal
![dublin](https://github.com/lumarcinkowski/object-detection/assets/162375638/1a3affb8-637f-4826-a129-27e7e2d01b97)


2. Image Processing Operations:

img = np.abs(imgOriginal.astype(int) - imgEdited.astype(int)).astype(np.uint8)

imgInGray = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])

imgThresh = np.zeros_like(imgInGray)

threshold = 10

imgThresh[imgInGray > threshold] = 255


This section calculates the absolute difference between the original and edited images, converts them to grayscale, and applies a threshold to create a binary image (imgThresh), where pixel values above a certain threshold are set to 255.


4. Find Contours:
Loop iterates over each pixel in the binary image (imgThresh) and identifies contour points by checking if a pixel is white and if its neighboring pixels are black.


5. Group Contours:
Group contours into objects based on their proximity to each other.
6. Find Largest Object:
7. Draw Bounding Box:

![bounding_box](https://github.com/lumarcinkowski/object-detection/assets/162375638/fb82f52a-b5b4-4ad7-8e15-caeb4d5b1437)
