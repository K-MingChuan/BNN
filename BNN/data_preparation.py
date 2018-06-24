import os
from collections import namedtuple
from scipy import misc

import requests

from image_preprocessing import create_normalized_image_dict, create_student_image_dict
from image_preprocessing import read_all_prediction_images

eportfolio_url_prefix = "https://www.mcu.edu.tw/student/%E6%A0%A1%E5%9C%92IC%E5%8D%A1%E7%85%A7%E7%89%87%E6%AA%94/student/"


def crawl_and_save_all_student_pictures(target_dir="pics"):
    """
    :param target_dir: output file directory name
    """
    ids = read_all_students_id()
    i = 0
    for id in ids:
        url = eportfolio_url_prefix + id + ".jpg"
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(target_dir + '/' + id + ".jpg", 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        i += 1
        print(str(i) + " pictures saved.")


def read_all_students_id():
    """
    :return: all students' ids
    """
    ids = []
    with open('students_score.txt', 'r', encoding='utf-8') as file:
        for s in file.readlines():
            s = s.strip()
            if len(s) != 0:
                fields = s.split(' ')
                txt = fields[0]
                if len(txt) != 8:
                    continue
                ids.append(txt)
    return ids


def read_all_students(normalized=False):
    """
    :param normalized: if normalized, all pictures will be resized into the same size corresponding to the smallest size of all pictures
    :return: a list of students, each student is a namedtuple of (id, name, gender, image)
    """
    Student = namedtuple('Student', 'id score image')
    StudentId = namedtuple('StudentId','id score')

    students_images_ids= read_all_id_images()

    # student_ids = read_all_students_id()
    # student_imgs_dict = create_normalized_image_dict(student_ids) if normalized \
    #                         else create_student_image_dict(student_ids)
    students = []
    studentsall = []
    with open('students_score.txt') as file:
        for s in file.readlines():
            s = s.strip()
            if len(s) != 0:
                fields = s.split(' ')
                if len(fields) != 2:
                    continue
                id = fields[0]
                score = int(fields[1])
                # img = student_imgs_dict[id]
                # students.append(Student(id, score, img))
                students.append(StudentId(id,score))

    students =check_images_in_id(students,students_images_ids)

    for student in students:
        path = 'face_pics_resized/second_folder/' + student.id + '.jpg'
        img = misc.imread(path)
        studentsall.append(Student(student.id,student.score,img))


    return studentsall


def check_images_in_id(students, images):
    checked = []
    for student in students:
        if student.id in images:
            checked.append(student)
    return checked

def get_all_prediction_students():
    Students = namedtuple('Student', 'id image')
    imagesId = read_all_id_images()
    students = []
    for student in imagesId:
        path = 'face_pics_resized/second_folder/' + student + '.jpg'
        img = misc.imread(path)
        students.append(Students(student,img))

    return students


def read_all_id_images(directory='face_pics_resized/second_folder'):
    """
        :return: all students' ids

        """
    imagesId = []
    filenames = os.listdir(directory)
    for filename in filenames:
        filename = filename.strip()
        if len(filename) != 0:
            fields = filename.split('.')
            if len(fields) != 2:
                continue
            id = fields[0]
            imagesId.append(id)
    return imagesId

if __name__ == '__main__':
    crawl_and_save_all_student_pictures()