from flask import jsonify
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os


def enhance_image(image_file):
    try:
        # Define the relative path to the model
        relative_path = os.path.join(os.path.dirname(__file__), "DSRCNN.keras")

        # Load the model using the relative path
        model = tf.keras.models.load_model(relative_path, compile=False)
    except Exception as e:
        return jsonify({"Error": f"Error loading model: {e}"}), 500

    try:
        # Loads the received file path as an image
        image = tf.keras.utils.load_img(io.BytesIO(image_file.read()), color_mode="rgb")
    except Exception as e:
        return jsonify({"Error": f"Error loading image: {e}"}), 500

    try:
        # Converts the image into an array of numbers the model can process
        image_array = tf.keras.utils.img_to_array(image)
        image_array = image_array.astype('float32') / 255.0

        # Makes the model prediction and returns it to an image
        enhanced_image_array = model.predict(np.expand_dims(image_array, axis=0))[0]
        enhanced_image_array = np.clip(enhanced_image_array * 255.0, 0, 255).astype('uint8')

        enhanced_image = Image.fromarray(enhanced_image_array, 'RGB')
    except Exception as e:
        return jsonify({"Error": f"Error processing image: {e}"}), 500

    return enhanced_image
