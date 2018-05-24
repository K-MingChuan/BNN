import json

import cognitive_face as CF
import requests
import time

from data_preparation import read_all_students_id


BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

BASE_EP_URL = 'https://www.mcu.edu.tw/student/%E6%A0%A1%E5%9C%92IC%E5%8D%A1%E7%85%A7%E7%89%87%E6%AA%94/student/{}.jpg'

headers = {'Ocp-Apim-Subscription-Key': 'b1df62838fcd4a96a56ebbecfd81f532' }

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

with open('all_faces.json', 'r', encoding='utf-8') as fr:
    all_faces = json.load(fr)
for student_id in read_all_students_id():
    time.sleep(3)
    img_url = BASE_EP_URL.format(student_id)
    response = requests.post(BASE_URL, params=params, headers=headers, json={"url": img_url})
    faces = response.json()
    all_faces.append(faces)
    with open('all_faces.json', 'w+', encoding='utf-8') as fw:
        json.dump(all_faces, fw)
    print(str(len(all_faces)) + " students' faces saved.")

