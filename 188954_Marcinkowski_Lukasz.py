import cv2
import numpy as np

imgEdit = "dublin_edited.jpg"
imgOrg = "dublin.jpg"
imgEdited = cv2.imread(imgEdit)
imgOriginal = cv2.imread(imgOrg)


img = np.abs(imgOriginal.astype(int) - imgEdited.astype(int)).astype(np.uint8)
imgInGray = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
imgThresh = np.zeros_like(imgInGray)

threshold = 10
imgThresh[imgInGray > threshold] = 255

#Wykrycie konturow
contours = []
for i in range(1, imgThresh.shape[0]-1):
    for j in range(1, imgThresh.shape[1]-1):
        if imgThresh[i, j] == 255:
            if imgThresh[i-1, j] == 0 or imgThresh[i+1, j] == 0 or imgThresh[i, j-1] == 0 or imgThresh[i, j+1] == 0:
                contours.append((j, i))


#Stworzenie obiektow z konturow
odleglosc = 20
objects = []
for contour in contours:
    added = False
    for obj in objects:
        if len(obj) == 0:
            obj.append(contour)
            added = True
            break
        else:
            distances = [np.sqrt((x - contour[0]) ** 2 + (y - contour[1]) ** 2) for x, y in obj]
            if min(distances) < odleglosc:
                obj.append(contour)
                added = True
                break
        if added:
            break
    if not added:
        objects.append([contour])

maks = 0
kevin = []
#Rysuj bounding boxy
for object in objects:
    min_x = min(object, key=lambda x: x[0])[0]
    max_x = max(object, key=lambda x: x[0])[0]
    min_y = min(object, key=lambda y: y[1])[1]
    max_y = max(object, key=lambda y: y[1])[1]

    imgEdited[min_y:max_y, min_x] = [255, 3, 184]
    imgEdited[min_y:max_y, max_x] = [255, 3, 184]
    imgEdited[min_y, min_x:max_x] = [255, 3, 184]
    imgEdited[max_y, min_x:max_x] = [255, 3, 184]
    #Liczy pole i wybiera najwiekszy prostokat na zdjeciu
    if np.abs((max_x - min_x) * (max_y - min_y)) > maks:
        maks = np.abs((max_x - min_x) * (max_y - min_y))
        kevin = object



min_x = min(kevin, key=lambda x: x[0])[0]
max_x = max(kevin, key=lambda x: x[0])[0]
min_y = min(kevin, key=lambda y: y[1])[1]
max_y = max(kevin, key=lambda y: y[1])[1]
imgBox = imgEdited[min_y:max_y, min_x:max_x]
imgBoxThresh = imgThresh[min_y:max_y, min_x:max_x]
imgBox = imgBox[1:-1, 1:-1]
imgBoxThresh = imgBoxThresh[1:-1, 1:-1]

#dodaj kanal alfa do wycietego Kevina
h, w = imgBox.shape[:2]
alpha = np.full((h, w, 1), 255, dtype=np.uint8)
imgBoxAlpha = np.dstack((imgBox, alpha))

cv2.imwrite('maska_przed_przekszatlceniami.jpg', imgBoxThresh)

kernel = np.ones((2, 2), np.uint8)
imgPadded = np.pad(imgBoxThresh, kernel.shape[0] // 2)
imgDilated = np.zeros_like(imgBoxThresh)

#Dylatacja
for i in range(imgBoxThresh.shape[0]):
    for j in range(imgBoxThresh.shape[1]):
        shifted = imgPadded[i:i + kernel.shape[0], j:j + kernel.shape[1]] * kernel
        imgDilated[i, j] = np.max(shifted)
imgPadded = np.pad(imgDilated, kernel.shape[0] // 2)
#Erozja
for i in range(imgBoxThresh.shape[0]):
    for j in range(imgBoxThresh.shape[1]):
        shifted = imgPadded[i:i + kernel.shape[0], j:j + kernel.shape[1]] * kernel
        imgDilated[i, j] = np.min(shifted)

for i in range(1, imgBox.shape[0]-1):
    for j in range(1, imgBox.shape[1]-1):
        if (imgDilated[i, j] != [255, 255, 255, 255]).all():
            imgBoxAlpha[i, j] = [0, 0, 0, 0]
imgBoxAlpha = imgBoxAlpha[1:-1, 1:-1]

cv2.imshow('obraz_prostokaty.jpg', imgEdited)
cv2.imwrite('dublin_gotowy.jpg', imgEdited)
cv2.imwrite('kevin.png', imgBoxAlpha)
cv2.imwrite('maska.jpg', imgDilated)


cv2.waitKey(0)
cv2.destroyAllWindows()

