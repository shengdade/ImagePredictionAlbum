import numpy as np
from keras.preprocessing import image

from deep_models.imagenet_utils import preprocess_input, decode_predictions
from deep_models.resnet50 import ResNet50


def classify_image(img_path):
    model = ResNet50(weights='imagenet')

    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    return decode_predictions(preds)
