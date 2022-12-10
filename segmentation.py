#https://github.com/anish9/Fashion-AI-segmentation 의류 인식후 잘라내기

from keras.models import load_model
import tensorflow as tf
import numpy as np
import cv2

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth=True
session = tf.compat.v1.Session(config=config)

saved = load_model("save_ckp_frozen.h5")
#h5라는 파일인데 keras을 통해 CNN등의 딥러닝 모델을 만들어
#이를 학습시켜 파일로 저장해 놓은것입니다.


class fashion_tools(object):
    def __init__(self,imageid,model,version=1.1):
        self.imageid = imageid
        self.model   = model
        self.version = version

    def get_dress(self,stack=False):

        name = self.imageid
        file = cv2.imread(name)
        file = tf.image.resize_with_pad(file,target_height=512,target_width=512)
        rgb = file.numpy()
        file = np.expand_dims(file,axis=0)/ 255.
        seq = self.model.predict(file)
        seq = seq[3][0,:,:,0]
        seq = np.expand_dims(seq,axis=-1)
        c1x = rgb*seq
        c2x = rgb*(1-seq)
        cfx = c1x+c2x
        dummy = np.ones((rgb.shape[0],rgb.shape[1],1))
        rgbx = np.concatenate((rgb,dummy*255),axis=-1)
        rgbs = np.concatenate((cfx,seq*255.),axis=-1)

        if stack:
            stacked = np.hstack((rgbx,rgbs))
            return stacked
        else:
            return rgbs

    def get_patch(self):
        return None


###running code

# f ="shorts.jpg"
# f ="sneakers.jpg"
# f ="slacks.jpg"
# f ="short_sleeve.jpg"
# f ="shirts.jpg"
# f ="long_sleeve.jpg"
# f ="jeans.jpg"
# f ="jacket.jpg"
# f ="hoodie.jpg"
# f ="hat.jpg"
# f ="dress_shoes.jpg"
# f ="cotton_pants.jpg"
f ="coat.jpg"
# f ="cardigan.jpg"
# f ="test.jpg"

api = fashion_tools("img_src/"+f,saved)
image_ = api.get_dress(stack=False)
cv2.imshow("image_",image_)
cv2.waitKey(0)
cv2.imwrite(f"img/{f[:-3]}png",image_)
