import color_extraction
import image_open
import remove_background

url = 'https://image.msscdn.net/images/goods_img/20221123/2958053/2958053_1_500.jpg?t=20221206133853'
image = image_open.img_url_open(url, True)
image = remove_background.image_remove(image, True)

color_hsv = color_extraction.extract(image, True)
print(color_hsv)

# tag = tagging(color)
