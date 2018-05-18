from collections import namedtuple

import requests

from image_preprocessing import create_normalized_image_dict, create_student_image_dict
eportfolio_url_prefix = "https://www.mcu.edu.tw/student/%E6%A0%A1%E5%9C%92IC%E5%8D%A1%E7%85%A7%E7%89%87%E6%AA%94/student/"


def crawl_and_save_all_student_pictures(target_dir="pics"):
    """
    :param target_dir: output file directory name
    """
    ids = read_all_students_id()
    for id in ids:
        url = eportfolio_url_prefix + id + ".jpg"
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(target_dir + '/' + id + ".jpg", 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)


def read_all_students_id():
    """
    :return: all students' ids
    """
    ids = []
    with open('students.txt') as file:
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
    Student = namedtuple('Student', 'id name gender image')
    student_ids = read_all_students_id()
    student_imgs_dict = create_normalized_image_dict(student_ids) if normalized \
                            else create_student_image_dict(student_ids)
    students = []

    with open('students.txt') as file:
        for s in file.readlines():
            s = s.strip()
            if len(s) != 0:
                fields = s.split(' ')
                if len(fields) != 3:
                    continue
                id = fields[0]
                name = fields[1]
                gender = int(fields[2])
                img = student_imgs_dict[id]
                students.append(Student(id, name, gender, img))
    return students
