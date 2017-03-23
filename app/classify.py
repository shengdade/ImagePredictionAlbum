import time

import numpy as np
from keras.preprocessing import image

from app.deep_models.imagenet_utils import preprocess_input, decode_predictions
from app.deep_models.vgg16 import VGG16
from app.deep_models.resnet50 import ResNet50
from app.deep_models.vgg19 import VGG19


def classify_image(img_path):
    model = VGG16(weights='imagenet')

    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    return decode_predictions(preds)


if __name__ == '__main__':
    test_image_path = './static/elephant.jpg'
    start_time = time.time()
    print(classify_image(test_image_path))
    elapsed_time = time.time() - start_time
    print('\nTime for prediction: ' + str(elapsed_time) + ' seconds')
