import matplotlib.pyplot as plt
from skimage import io
import cv2.cv2 as cv2
import os

def img_url_open(url, view=False): # 이미지 URL을 열어 numpy.ndarray 반환(RGB)
    try:
        image = io.imread(url)
        if view:
            plt.imshow(image)
            plt.show()

        return image

    except:
        print("이미지 url 읽기 실패")
        print(f'url : {url}')

        return -1

def img_file_open(file_path, view=False): # 이미지 파일을 열어 numpy.ndarray 반환(RGB)
    try:
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if view:
            plt.imshow(image)
            plt.show()

        return image

    except:
        print("이미지 path 읽기 실패")
        print(f'file_path : {file_path}')

        return -1

def img_dir_open(dir_path, view=False): # 이미지 폴더를 열어 numpy.ndarray 배열 반환(RGB)
    try:
        file_list = os.listdir(dir_path)
        file_path = ""

        result = []

        for file_path in file_list:
            image = cv2.imread(f'{dir_path}/{file_path}')
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result.append(image)
            if view:
                plt.imshow(image)
                plt.show()

        return result

    except:
        print("폴더 내 이미지 path 읽기 실패")
        print(f'dir_path : {dir_path}')
        print(f'file_path : {file_path}')

        return -1

if __name__ == "__main__":
    img_url_open('https://cdn.imweb.me/thumbnail/20211105/16246701edcd5.jpg', True)
    img_file_open('img/hoodie.png', True)
    img_dir_open('img', True)