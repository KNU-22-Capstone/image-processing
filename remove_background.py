import cv2.cv2 as cv2
import matplotlib.pyplot as plt
from rembg import remove, new_session

session = new_session()


def image_remove(image, view=False):
    try:
        output = remove(image, session=session)

        if view:
            plt.imshow(output)
            plt.show()

        return output

    except:
        print("배경제거 실패")
        return -1


if __name__ == "__main__":
    image = cv2.imread('img/hoodie.png')
    image_remove(image, True)
