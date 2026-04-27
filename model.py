import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from PIL import Image, ImageOps
import numpy as np


def build_model(num_classes: int = 4) -> tf.keras.Model:
    base = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights=None,
        pooling='avg',
        alpha=0.35,
        classes=num_classes,
    )

    head = models.Sequential(
        [
            layers.Dense(100, activation='relu', name='dense_Dense3'),
            layers.Dense(num_classes, use_bias=False, activation='softmax', name='dense_Dense4'),
        ],
        name='sequential_7',
    )

    model = models.Sequential([base, head], name='sequential_5')
    return model


def get_class(model_path, labels_path, image_path):
    model = build_model(num_classes=4)
    model.load_weights(model_path)

    np.set_printoptions(suppress=True)
    class_names = open(labels_path, "r", encoding="utf-8").readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(image_path).convert("RGB")

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name.strip(), float(confidence_score)
