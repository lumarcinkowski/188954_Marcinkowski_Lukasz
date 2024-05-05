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


This code calculates the absolute difference between the original and edited images, converts them to grayscale, and applies a threshold to create a binary image (imgThresh), where pixel values above a certain threshold are set to 255.


3. Find Contours:
Loop iterates over each pixel in the binary image (imgThresh) and identifies contour points by checking if a pixel is white and if its neighboring pixels are black.


4. Group Contours:
Group contours into objects based on their proximity to each other.


5. Draw Bounding Box around objects:
![bounding_box](https://github.com/lumarcinkowski/object-detection/assets/162375638/fb82f52a-b5b4-4ad7-8e15-caeb4d5b1437)


6. Find largest object
The next step is to find the largest object and cut it out of the image.

7.Cut out the largest image without the background
Use dilatation operation 
Mask of the image
 ![maska](https://github.com/lumarcinkowski/object-detection/assets/162375638/03f96f29-ee90-45eb-a41d-466e0e132e46)

 
Image without background
 ![wyciety_kevin](https://github.com/lumarcinkowski/object-detection/assets/162375638/a5186266-1bc1-4f7e-961f-39c4b4fa4e70)




