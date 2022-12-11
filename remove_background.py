import matplotlib.pyplot as plt
from rembg import remove, new_session
from skimage import io
session = new_session()

def img_url_to_remove(url):
    try:
        image = io.imread(url)
        plt.imshow(image)
        plt.show()
    except:
        print("이미지 url 읽기 실패")
        print(f'url : {url}')
        return -1
    try:
        output = remove(image, session=session)
        plt.imshow(output)
        plt.show()
    except:
        print("배경제거 실패")
        return -2
    return output

if __name__ == "__main__":
    image = img_url_to_remove('https://www.shutterstock.com/image-photo/serving-pizza-food-photography-recipe-600w-1199267023.jpg')
    plt.imshow(image)
    plt.show()
