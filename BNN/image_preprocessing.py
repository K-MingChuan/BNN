import os
import io
from PIL import Image
from scipy import misc
from collections import namedtuple


def create_normalized_image_dict(student_ids, resize=None):
    """
    :param student_ids: all students' ids
    :param resize: the size tuple (width, height), find the smallest size of all pictures if not specified
    :return: normalized image dict which the student id is the key and his picture array is the value
    """
    if not resize:
        imgs = read_all_images()
        resize = find_smallest_size(imgs)

    resize_all_images_and_save(imgs, resize)

    s_dict = {}

    for student_id in student_ids:
        path = 'face_pics_resized/second_folder/' + student_id + '.jpg'
        img = misc.imread(path)
        s_dict[student_id] = img
    return s_dict


def create_student_image_dict(student_ids):
    """
    :param student_ids: all students' ids
    :return: unnormalized image dict which the student id is the key and his picture array is the value
    """

    s_dict = {}
    for student_id in student_ids:
        path = 'face_pics_resized/second_folder/' + student_id + '.jpg'
        img = misc.imread(path)
        s_dict[student_id] = img
    return s_dict

def read_all_prediction_images(directory='face_pics_resized/second_folder'):
    imgs = []
    filenames = os.listdir(directory)
    for i in range(0,9000):
        filenames.pop(0)

    for filename in filenames:
        imgs.append(Image.open(directory + '/' + filename))
    return imgs

def read_all_images(directory='face_pics_resized/second_folder'):
    """
    :return: all images under specific directory, if no directory specified, 'pics' used as default
    """

    imgs = []
    filenames = os.listdir(directory)
    for filename in filenames:
        imgs.append(Image.open(directory + '/' + filename))

    return imgs

def read_all_id_images(directory='face_pics_resized/second_folder'):

    StudentsId = namedtuple('StudentsId', 'id')
    imagesId = []
    filenames = os.listdir(directory)
    for filename in filenames:
        filename = filename.strip()
        if len(filename) != 0:
            fields = filename.split('.')
            if len(fields) != 2:
                continue
            id = fields[0]
            imagesId.append(StudentsId(id))
    return imagesId

def find_smallest_size(images):
    """
    :param images: all PIL images
    :return: the smallest size tuple (width, height)
    """
    smallest_size = (999999, 999999)
    for image in images:
        size = image.width, image.height
        if size[0] < smallest_size[0] and size[1] < smallest_size[1]:
            smallest_size = size
    return smallest_size


def resize_all_images_and_save(images, resize):
    """
    this method will resize and save back the images.
    :param images: all PIL images
    :param resize: the size tuple (width, height) specified to resize to
    """
    for image in images:
        filename = image.filename
        image = image.resize(resize, Image.BILINEAR)
        image.save(filename)


