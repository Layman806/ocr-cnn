import h5py
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import keras
import numpy as np
import cv2
import string
import jsonio as jio

img_width = 64
img_height = 64

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))

model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(36))
model.add(Activation('softmax'))

opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

# loading saved model
model.load_weights('third_try.h5')
'''
# loading saved classes list for model, by generating test data first
test_datagen = ImageDataGenerator(rescale=1./255)

batch_size = 16
validation_generator = test_datagen.flow_from_directory(
        'Test',
        target_size=(64, 64),
        batch_size=batch_size,
        class_mode='categorical')
'''
class_labels = jio.get('classnames.txt')
# print(class_labels)


def predict(img):
    img = cv2.resize(img, (img_height, img_width))
    img = np.reshape(img, [1, img_height, img_width, 3])
    pr = model.predict(img)
    pr_i = np.argmax(pr)
    actual_i = int(class_labels[pr_i])
    pr_i = actual_i
    '''Code to return class name based on predicted index, pr_i'''
    # print(pr_i)
    if pr_i < 10:
        return str(pr_i)
    else:
        return list(string.ascii_uppercase)[pr_i-10]


# Usage example:
im = cv2.imread('13.png')
print(predict(im))

