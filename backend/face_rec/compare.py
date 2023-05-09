# -*- coding: utf-8 -*-
# @Time : 2021/12/3 15:46
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : pickle_load.py
# @Software: PyCharm
import os
import pickle

import PIL.Image
from rbac.models import User

import face_recognition

from PoliceTrainSystem.settings import MEDIA_ROOT, BASE_DIR
from utils.response import APIResponse


def compare(to_check_img):
    father_path = os.path.join(BASE_DIR,'face_rec')
    faces_encoding_path = os.path.join(father_path, "faces_encodings.pkl")
    file = open(faces_encoding_path, "rb")
    faces_encoding = pickle.load(file)
    file.close()
    try:
        to_check_img_encoding = face_recognition.face_encodings(face_image=to_check_img, num_jitters=3)
        if len(to_check_img_encoding) == 0:
            raise (Exception('图片中未识别到人脸'))
    except Exception as e:
        raise(ValueError(e))
    else:
        to_check_img_encoding = to_check_img_encoding[0]
        user_file_path = os.path.join(father_path, "faces_user.pkl")
        user_file = open(user_file_path, "rb")
        faces_user = pickle.load(user_file)
        user_file.close()
        user = None
        for index, each in enumerate(faces_encoding):
            result = face_recognition.compare_faces([each], to_check_img_encoding, tolerance=0.4)
            # print(result)
            if result[0] == True:
                user = faces_user[index]
                return user
        return user
