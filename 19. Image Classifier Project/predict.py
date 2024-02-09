import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_hub as hub
import warnings
import time
import numpy as np
import matplotlib.pyplot as plt
import json
import logging
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import argparse
from PIL import Image

batch_size = 32
image_size = 224

def format_image(image, label): 
    image = tf.cast(image, tf.float32)
    image = tf.image.resize(image, (image_size, image_size))
    image /= 255
    return image, label

def process_image(image):
    image = tf.image.resize(image, (image_size, image_size))
    image = tf.cast(image, tf.float32) / 255.0
    return image

def predict(image_path, model, top_k):
    img = Image.open(image_path)
    img_array = np.asarray(img)
    processed_image = process_image(img_array)
    processed_image = np.expand_dims(processed_image, axis=0)
    predictions = model.predict(processed_image)
    probs, labels = tf.nn.top_k(predictions, k=top_k)
    probs = list(probs.numpy()[0])
    labels = list(labels.numpy()[0])
    
    return probs, labels

parser = argparse.ArgumentParser()
parser.add_argument('--input', default='./test_images/hard-leaved_pocket_orchid.jpg', action="store", type = str, help='Path to Image folder')
parser.add_argument('--model', default='./image_classifier_model.h5', action="store", type = str, help='Path to saved model')
parser.add_argument('--top_k', default=5, action="store", type=int, help='Return the top K class probabilities')
parser.add_argument('--category_names', default='./label_map.json', action="store", type=str, help='Path to a JSON file mapping labels to flower names')

arg_parser = parser.parse_args()

image_path = arg_parser.input
model = arg_parser.model
top_k = arg_parser.top_k
category_names = arg_parser.category_names

if __name__== "__main__":
    with open(category_names, 'r') as f:
        class_names = json.load(f)

    reloaded_keras_model = tf.keras.models.load_model(model, custom_objects = {'KerasLayer':hub.KerasLayer})

    probs, labels = predict(image_path, reloaded_keras_model, top_k)
    print(probs)
    print(labels)


