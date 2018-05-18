import numpy as np
from keras.models import *
from keras.layers import *
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

from data_preparation import *

# crawl_and_save_all_student_pictures()  # use this method to crawl student pictures from the website

students = read_all_students(normalized=False)
all_images = np.array([student.image for student in students])
all_genders_ont_hot = np.array([[0, 1] if student.gender == 1 else [1, 0] for student in students])


count = len(students)
train_data = all_images[:count-30]
train_labels = all_genders_ont_hot[:count-30]
test_data = all_images[count-30:]
test_labels = all_genders_ont_hot[count-30:]

height, width, channel = train_data[0].shape
batch_size = 25

model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(height, width, channel)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization(axis=-1))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())

# Fully connected layer
model.add(Dense(512))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(2))
model.add(Softmax())

model.summary()

model.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])


gen = ImageDataGenerator(rotation_range=8, width_shift_range=0.08, shear_range=0.3, height_shift_range=0.08, zoom_range=0.08)
test_gen = ImageDataGenerator()

train_generator = gen.flow(train_data, train_labels, batch_size=batch_size)
test_generator = test_gen.flow(test_data, test_labels, batch_size=batch_size)

model.fit_generator(train_generator, steps_per_epoch=train_labels.shape[0]//batch_size, epochs=12,
                    validation_data=test_generator, validation_steps=test_labels.shape[0]//batch_size)

score = model.evaluate(test_data, test_labels)

print('Test accuracy: ', score[1])
