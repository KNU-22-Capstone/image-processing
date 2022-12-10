import cv2, sys
import numpy as np

def edge(src):
    image = cv2.imread(src)
    cv2.imshow("show", image)
    cv2.waitKey(0)
    image_gray = cv2.imread(src, cv2.IMREAD_GRAYSCALE)

    blur = cv2.GaussianBlur(image_gray, ksize=(5,5), sigmaX=0)

    edged = cv2.Canny(blur, 10, 250)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours_xy = np.array(contours)
    contours_xy.shape

    x_min, x_max = 0, 0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(contours_xy[i][j][0][0])  # 네번째 괄호가 0일때 x의 값
            x_min = min(value)
            x_max = max(value)

    y_min, y_max = 0, 0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(contours_xy[i][j][0][1])  # 네번째 괄호가 0일때 x의 값
            y_min = min(value)
            y_max = max(value)

    x = x_min
    y = y_min
    w = x_max-x_min
    h = y_max-y_min

    img_trim = image[y:y + h, x:x + w]

    print('img/' + src[8:])

    cv2.imwrite('img/' + src[8:], img_trim)
    cv2.imshow('img_trim', img_trim)
    cv2.waitKey(0)

    # org_image = cv2.imread('img/'+src[8:])
    # cv2.imshow('org_image', org_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

edge('img/test.png')