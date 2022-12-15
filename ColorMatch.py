import colorsys

import cv2
import matplotlib.image as mpimg
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

import image_open
import remove_background as rb


# -------------------------------------------현재 색상의 빈도에 따라 bar를 만드는 함수------------------------------
def plot_colors(hist, centroids):
    # 각 색상의 상대 빈도를 나타내는 막대 차트 초기화

    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0
    maxvalue = 0

    # 각 클러스터의 백분율과 색상을 반복합니다.
    # zip은 병렬처리할때 여러 그룹의 데이터를 루프한번만 돌면서 처리 가능하다.(두 그룹의 데이터를 서로 엮어주는 것)
    for (percent, color) in zip(hist, centroids):
        # 각 군집의 상대 백분율을 표시합니다.
        endX = startX + (percent * 300)
        # startX는 bar의 처음부분 endx는 bar의 마지막 좌표부분임 그래서 막대의 크기를 통해 가장 많은색상을 비교해 추출함
        if (maxvalue < (endX - startX)):
            maxvalue = endX
            maxcolor = color
        maxcolor = maxcolor.astype(int)  # 여기가 가장 많은색상을 추출하는곳

        # 사각형으로 만듬
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    return bar, maxcolor


# -------------------------------------------k값에 따라 bar를 통해 빈도가 높은 색상을 표현------------------------------
def image_color_cluster(url, checking, k=3):
    # def image_color_cluster(image_path, checking, k=5):
    # image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = image.reshape((image.shape[0] * image.shape[1], 3))

    # 이미지 url 열기
    image = image_open.img_url_open(url)

    # 배경 제거(투명화)
    image = rb.image_remove(image)

    # 4채널값 투명도가 1 이상인 경우만 추가
    temp = []
    for i in image:
        for j in i:
            if j[3] > 1:
                temp.append([j[0], j[1], j[2]])

    # 클러스터 생성 (n_clusters = k)는 정해진 명령어(fit로 클러스터링함)
    clt = KMeans(n_clusters=k)
    clt.fit(np.array(temp))

    # 클러스터의 수를 파악하고 히스토그램을 만듬(각 클러스터에 할당된 픽셀 수를 기반으로)
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # 합이 1이 되도록 히스토그램을 정규화합니다.
    hist = hist.astype("float")
    hist /= hist.sum()

    bar, maxcolor = plot_colors(hist, clt.cluster_centers_)
    if (checking == True):
        plt.figure()
        plt.axis("off")
        plt.imshow(bar)
        plt.show()

    return maxcolor


# -------------------------------------------rgb값을 HSV값으로 바꾸는 함수------------------------------
def convert_rgb_to_hsv(r, g, b):
    # rgb기본 범위: (0-255, 0-255, 0.255)

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
    color_hsv = (color_h, color_s, color_v)

    return color_hsv


# -----------------------------메인부분---체크하는 의류(상의)--------------------------------------
# 여기가 내가 선택한 상의를 넣는 곳 상의를 넣게되면 저장되어 있는 하의들과 비교하는 시나리오임

# chkimg ="shorts.jpg"
# chkimg ="sneakers.jpg"
# chkimg ="slacks.jpg"
# chkimg ="short_sleeve.jpg"
# chkimg ="shirts.jpg"
# chkimg ="long_sleeve.jpg"
# chkimg ="jeans.jpg"
# chkimg ="jacket.jpg"
# chkimg ="hoodie.jpg"
chkimg = "hat.jpg"
# chkimg ="dress_shoes.jpg"
# chkimg ="cotton_pants.jpg"
# chkimg ="coat.jpg"
# chkimg ="cardigan.jpg"
# chkimg ="test.jpg"

image = mpimg.imread("img/" + chkimg[:-3] + "png")
plt.imshow(image)
# up_color = image_color_cluster("img/"+chkimg[:-3]+"png", True)  # TRUE는 해당 bar를 보여주게끔한다.밑에서는 생략하려고 함
up_color = image_color_cluster("https://cdn.imweb.me/upload/S201612025840bcf9c3866/4f56d1796c287.jpeg",
                               True)  # TRUE는 해당 bar를 보여주게끔한다.밑에서는 생략하려고 함
print("체크하는 의류 BRG Format: ", up_color)
up_hsv_color = convert_rgb_to_hsv(up_color[0], up_color[1], up_color[2])
print("저장되는 의류 HSV Format", up_hsv_color)
