import color_extraction
import image_open
import remove_background
import ton_tag

# url = 'https://image.msscdn.net/images/goods_img/20221123/2958053/2958053_1_500.jpg?t=20221206133853' #무채색 신발
url = 'https://image.msscdn.net/images/goods_img/20180917/859956/859956_9_500.jpg'
image = image_open.img_url_open(url, True)

image = remove_background.image_remove(image, True)

color_hsv = color_extraction.extract(image, True)
print(color_hsv)
tag = ton_tag.tagging(color_hsv)
print(tag)

# image = image_open.img_dir_open("img_src")
# for i in image:
#     img = remove_background.image_remove(i, True)
#     color_hsv = color_extraction.extract(img, True)
