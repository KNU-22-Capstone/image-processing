import colorsys

import cv2
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

import image_open
import remove_background


def extract(image, view=False, k=3):  # 색추출 메인 함수
    try:
        up_color = image_color_cluster(image, view, k)

        if view:
            print("체크하는 의류 BRG Format: ", up_color)

    except Exception as e:
        print("\n색추출 실패")
        print(e)
        return -1

    try:
        up_hsv_color = convert_rgb_to_hsv(up_color[0], up_color[1], up_color[2])

        if view:
            print("저장되는 의류 HSV Format", up_hsv_color)

        return up_hsv_color

    except:
        print("rgb to hsv 변환 실패")
        return -1


def convert_rgb_to_hsv(r, g, b):
    # get rgb percentage: range (0-1, 0-1, 0-1 )
    red_percentage = r / float(256)
    green_percentage = g / float(256)
    blue_percentage = b / float(256)

    # get hsv percentage: range (0-1, 0-1, 0-1)
    color_hsv_percentage = colorsys.rgb_to_hsv(red_percentage, green_percentage, blue_percentage)

    # get normal hsv: range (0-360, 0-255, 0-255)
    color_h = round(360 * color_hsv_percentage[0])
    color_s = round(100 * color_hsv_percentage[1])
    color_v = round(100 * color_hsv_percentage[2])

    return (color_h, color_s, color_v)


def plot_colors(hist, centroids):  # 히스토그램을 막대 bar로 만들고, 최대빈도 컬러값 반환

    bar = np.zeros((50, 300, 3), dtype="uint8")  # 각 색상의 상대 빈도를 나타내는 막대 차트 초기화
    startX = 0  # bar의 시작 좌표
    maxvalue = 0

    for (percent, color) in zip(hist, centroids):  # 각 클러스터의 백분율과 색상을 반복

        # bar의 끝 좌표 : 각 군집의 상대 백분율을 표시
        endX = startX + (percent * 300)

        # 막대의 크기를 통해 가장 많은색상을 비교해 추출함
        if maxvalue < (endX - startX):
            maxvalue = endX
            maxcolor = color

        maxcolor = maxcolor.astype(int)  # 최대빈도 컬러값

        # 사각형으로 만듬
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    return bar, maxcolor


def image_color_cluster(image, view, k):  # 이미지의 컬러값을 클러스터 수(k) 대로 나누고, 최대빈도 컬러값을 반환
    # 4채널값이 있으면 투명도가 1 이상인 경우만 추가
    temp = []
    if len(image[0][0]) > 3:
        for i in image:
            for j in i:
                if j[3] > 1:
                    temp.append([j[0], j[1], j[2]])
    else:
        raise Exception(" >> 채널값이 3개 이하 : 배경제거 먼저하기")

    # 클러스터 생성 (n_clusters = k)는 정해진 명령어(fit로 클러스터링)
    clt = KMeans(n_clusters=k)
    clt.fit(np.array(temp))

    # 클러스터의 수를 파악하고 히스토그램을 생성(각 클러스터에 할당된 픽셀 수 기반)
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    hist, _ = np.histogram(clt.labels_, bins=numLabels)

    # 합이 1이 되도록 히스토그램을 정규화
    hist = hist.astype("float")
    hist /= hist.sum()

    bar, maxcolor = plot_colors(hist, clt.cluster_centers_)

    if view:
        plt.figure()
        plt.axis("off")
        plt.imshow(bar)
        plt.show()

    return maxcolor


if __name__ == "__main__":
    image = image_open.img_file_open('img/hoodie.png')
    image = remove_background.image_remove(image, True)
    extract(image, True, 3)

    extract(cv2.imread('img/coat.png'))  # 채널값 오류
