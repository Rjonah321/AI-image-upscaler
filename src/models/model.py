from tensorflow.keras.layers import Conv2D, Input, Conv2DTranspose, Add
from sklearn.model_selection import train_test_split
from tensorflow.keras import Model, optimizers
from pathlib import Path
import tensorflow as tf
from skimage import io
import numpy as np


# Define function for psnr metric
def psnr(y_true, y_pred):
    mse = tf.reduce_mean((y_true - y_pred) ** 2)
    return 20 * log10(1 / (mse ** 0.5))


# Define function for ssim metric
def ssim(y_true, y_pred):
    return tf.image.ssim(y_true, y_pred, max_val=1.0, filter_size=11, filter_sigma=1.5, k1=0.01, k2=0.03)


# Define a function for caluclating log10
def log10(x):
    numerator = tf.math.log(x)
    denominator = tf.math.log(tf.constant(10, dtype=numerator.dtype))
    return numerator / denominator


# Define a function that converts image paths to usable data
def load_data(paths):
    return np.array([io.imread(img_path)[:, :, :3] / 255.0 for img_path in paths])


if __name__ == "__main__":
    # Loads the data from specified directory
    data_dir = Path("../data/dataset_res256")
    X = list(data_dir.glob("low_quality/*"))
    y = list(data_dir.glob("high_quality/*"))

    X = load_data(X)
    y = load_data(y)

    # Splits the data into testing and training sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


    def dsrcnn(channels, upscale_factor=2):
        # Architecture for the DSRCNN model
        init = Input(shape=(None, None, channels))

        level1_1 = Conv2D(64, (3, 3), activation="relu", padding="same")(init)
        level2_1 = Conv2D(64, (3, 3), activation="relu", padding="same")(level1_1)

        level2_2 = Conv2DTranspose(64, (3, 3), activation="relu", padding="same")(level2_1)
        level2 = Add()([level2_1, level2_2])

        level1_2 = Conv2DTranspose(64, (3, 3), activation="relu", padding="same")(level2)
        level1 = Add()([level1_1, level1_2])

        decoded = Conv2DTranspose(channels, (upscale_factor * 2 + 1, upscale_factor * 2 + 1), strides=upscale_factor,
                                  activation="relu", padding="same")(level1)

        dsrcnn_model = Model(inputs=init, outputs=decoded)
        return dsrcnn_model


    # Loads model
    model = dsrcnn(3)

    # Compiles model using Adam optimizer and MeanSquaredError as the loss
    model.compile(optimizer=optimizers.Adam(0.001),
                  loss=tf.losses.MeanSquaredError(),
                  metrics=[psnr, ssim])

    # Fits the data to the model
    model.fit(X_train, y_train, epochs=50)

    # Evaluates the model and prints the results
    results = model.evaluate(X_test, y_test)
    print(f"Loss: {results[0]} - PSNR: {results[1]} - SSIM: {results[-1]}")

    # Saves the model
    model.save("DSRCNN.keras")
