import matplotlib.pyplot as plt
from rembg import remove, new_session
from skimage import io

session = new_session()

def oepn(url):
    try:
        image = io.imread(url)
        plt.imshow(image)
        plt.show()
        output = remove(image, session=session)
        print(type(output))
        plt.imshow(output)
        plt.show()

        return image
    except:
        print("이미지 url 읽기 실패")
        print(f'url : {url}')
        return -1

if __name__ == "__main__":
    image = io.imread('https://i.stack.imgur.com/yt0Xo.jpg')
    plt.imshow(image)
    plt.show()
