import time

import numpy as np
from keras.preprocessing import image

from .deep_models.imagenet_utils import preprocess_input, decode_predictions
from .deep_models.vgg16 import VGG16
from .deep_models.resnet50 import ResNet50
from .deep_models.vgg19 import VGG19
from .deep_models.inception_v3 import InceptionV3


def classify_image(img_path):
    model = VGG16(weights='imagenet')

    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    return decode_predictions(preds)


if __name__ == '__main__':
    test_image_path = 'app/static/elephant.jpg'
    start_time = time.time()
    print(classify_image(test_image_path))
    elapsed_time = time.time() - start_time
    print('\nTime for prediction: ' + str(elapsed_time) + ' seconds')
