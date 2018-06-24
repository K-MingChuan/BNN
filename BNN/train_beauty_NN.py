import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
import pylab as pl

from data_preparation import *

# crawl_and_save_all_student_pictures()  # use this method to crawl student pictures from the website

students = read_all_students(normalized=False)



prediction_students = get_all_prediction_students()

for student in students:
     if student.image.shape[2] != 3:
        print(student.id)

# 要被預測的學生
correct_prediction_students = []
c_i = []
# 把shape[2]不是3的都刪掉
for student in prediction_students:
    if student.image.shape[2] == 3 and student.id == "03360112":
        correct_prediction_students.append(student)
        c_i.append(student.image)

all_images = np.array([student.image for student in students])

prediction_image = np.array([student.image for student in correct_prediction_students])

score_label = np.array([[student.score] for student in students])

count = len(students)

prediction_count = len(prediction_image)

train_data = all_images[:count]  # 0 ~ 4971
train_labels = score_label[:count]

test_data = all_images[:count]
test_labels = score_label[:count]



pre_data = prediction_image[:prediction_count]


height, width, channel = train_data[0].shape

batch_size = 25

#
# model = Sequential()
#
# model.add(Conv2D(32, (3, 3), input_shape=(86, 86, 3)))
# model.add(BatchNormalization(axis=-1))
# model.add(Activation('relu'))
# model.add(Conv2D(32, (3, 3)))
# model.add(BatchNormalization(axis=-1))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
#
# # model.add(Conv2D(64,(3, 3)))
# # model.add(BatchNormalization(axis=-1))
# # model.add(Activation('relu'))
# model.add(Conv2D(64, (3, 3)))
# model.add(BatchNormalization(axis=-1))
# model.add(Activation('relu'))
# model.add(Conv2D(128, (3, 3)))
# model.add(BatchNormalization(axis=-1))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
#
# model.add(Flatten())
#
# # Fully connected layer
# model.add(Dense(512))
# model.add(BatchNormalization())
# model.add(Activation('relu'))
# model.add(Dropout(0.2))
# model.add(Dense(1))
#
# model.add(Activation('linear'))
#
# #print the model
# model.summary()
#
# #compile the model
# #定義訓練方式
# model.compile(loss='mean_squared_error', optimizer=Adam(), metrics=['mae'])
#
#
# # ImageDataGenerator 圖像擴增 (狂生猛生)
# gen = ImageDataGenerator(rotation_range=8, width_shift_range=0.08, shear_range=0.3, height_shift_range=0.08, zoom_range=0.08)
# test_gen = ImageDataGenerator()
#
# train_generator = gen.flow(train_data, train_labels, batch_size=batch_size)
# test_generator = test_gen.flow(test_data, test_labels, batch_size=batch_size)
#
# model.fit_generator(train_generator, steps_per_epoch=train_labels.shape[0]//batch_size, epochs=10,
#                     validation_data=test_generator, validation_steps=test_labels.shape[0]//batch_size)
#
# model.save('model_36_ep10.h5')

model = load_model('0617_100ep.h5')

# score = model.evaluate(test_data, test_labels)
#
# print('Test: ', score)

predictions = model.predict(pre_data, batch_size=32)
predictions_rank = list(predictions)
prediction_pos = list(predictions)
rank = []
rank_id = []
Student = namedtuple('Student', 'id score')

print(predictions_rank)

plt.figure()
plt.title(predictions_rank[0])
ax = plt.subplot(1, 1, 1)
ax.set_yticklabels([])
ax.set_xticklabels([])
plt.imshow(c_i[0])
plt.interactive(False)

plt.show()

#
#
# for i in range(0,50):
#     rank.append(Student(correct_prediction_students[predictions_rank.index(max(predictions_rank))].id, max(predictions_rank)))
#     rank_id.append(correct_prediction_students[predictions_rank.index(max(predictions_rank))].id)
#     predictions_rank[predictions_rank.index(max(predictions_rank))] = 0
#
# ix = 1
# for rs, ri in zip(rank, rank_id):
#     img = misc.imread('face_pics_resized/second_folder/' + ri + '.jpg')
#     plt.figure(1)
#     ax = plt.subplot(5, 10, ix)
#     ax.set_yticklabels([])
#     ax.set_xticklabels([])
#     plt.imshow(img)
#     print(rs)
#     ix += 1
#
# rank = []
# rank_id = []
# for i in range(0,50):
#     rank.append(Student(correct_prediction_students[prediction_pos.index(min(prediction_pos))].id, min(prediction_pos)))
#     rank_id.append(correct_prediction_students[prediction_pos.index(min(prediction_pos))].id)
#     prediction_pos[prediction_pos.index(min(prediction_pos))] = 100
#
# ix = 1
# for rs, ri in zip(rank, rank_id):
#     img = misc.imread('face_pics_resized/second_folder/' + ri + '.jpg')
#     plt.figure(2)
#     ax = plt.subplot(5, 10, ix)
#     ax.set_yticklabels([])
#     ax.set_xticklabels([])
#     plt.imshow(img)
#     print(rs)
#     ix += 1
#
# plt.interactive(False)
# plt.show()

# print(np.argmax(predictions))
# print(predictions[np.argmax(predictions)])
# print(np.amax(predictions))
# print(correct_prediction_students[np.argmax(predictions)].id)




