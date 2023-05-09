# -*- coding: utf-8 -*-
# @Time : 2021/12/2 17:03
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : test.py
# @Software: PyCharm


"""
1.加载数据库中所有的人脸
2.编码
3.传入一张图片和数据库中所有人脸进行比较
"""
"""
1.加载数据库中所有的人脸
2.编码
3.传入一张图片和数据库中所有人脸进行比较
"""

import logging
import face_recognition
import time
import pickle
from PoliceTrainSystem.settings import MEDIA_ROOT, BASE_DIR
from rbac.models import User
import os, sys
import django


def main():
    logger = logging.getLogger('log')

    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(parent_path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'PoliceTrainSystem.settings'
    django.setup()
    logger.info("正在加载人脸数据")
    st = time.time()
    face_directory_path = os.path.join(MEDIA_ROOT, 'face')
    if not os.path.exists(face_directory_path):
        os.mkdir(face_directory_path)
    user_dir = os.listdir(face_directory_path)
    known_names = []
    known_paths = []
    known_encodings = []
    for each in user_dir:
        uid = each
        user_imgs_path = os.path.join(face_directory_path, uid)
        image_file_list = os.listdir(user_imgs_path)
        for img in image_file_list:
            image_path = os.path.join(user_imgs_path, img)
            user = User.objects.filter(id=uid).first()
            known_names.append(user)
            known_paths.append(image_path)

    for path in known_paths:
        img = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(img, num_jitters=3)[0]
        known_encodings.append(encoding)

    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + '.')

    pickle_encodings_file = open(os.path.join(father_path, "faces_encodings.pkl"), 'wb')
    pickle.dump(known_encodings, pickle_encodings_file)
    pickle_encodings_file.close()

    pickle_name_file = open(os.path.join(father_path, "faces_user.pkl"), 'wb')
    pickle.dump(known_names, pickle_name_file)
    pickle_name_file.close()
    ed = time.time()
    duration = ed - st
    logger.info("人脸数据加载完成")


if __name__ == '__main__':
    main()

# def main():
#     logger = logging.getLogger('log')
#
#     import os, sys
#     parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     sys.path.append(parent_path)
#     os.environ['DJANGO_SETTINGS_MODULE'] = 'PoliceTrainSystem.settings'
#     import django
#     django.setup()
#     logger.info("正在加载人脸数据")
#     import face_recognition
#     import time
#     import pickle
#     from PoliceTrainSystem.settings import MEDIA_ROOT, BASE_DIR
#     from rbac.models import User
#
#     st = time.time()
#     face_directory_path = os.path.join(MEDIA_ROOT, 'face')
#     if not os.path.exists(face_directory_path):
#         os.mkdir(face_directory_path)
#     user_dir = os.listdir(face_directory_path)
#     known_names = []
#     known_paths = []
#     known_encodings = []
#     for each in user_dir:
#         uid = each
#         user_imgs_path = os.path.join(face_directory_path, uid)
#         image_file_list = os.listdir(user_imgs_path)
#         for img in image_file_list:
#             image_path = os.path.join(user_imgs_path, img)
#             user = User.objects.filter(id=uid).first()
#             known_names.append(user)
#             known_paths.append(image_path)
#
#     print("{:.<40}".format('[INFO] 人脸信息编码'))
#     for path in known_paths:
#         img = face_recognition.load_image_file(path)
#         encoding = face_recognition.face_encodings(img, num_jitters=3)[0]
#         known_encodings.append(encoding)
#
#     current_path = os.path.abspath(__file__)
#     father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + '.')
#
#     pickle_encodings_file = open(os.path.join(father_path, "faces_encodings.pkl"), 'wb')
#     pickle.dump(known_encodings, pickle_encodings_file)
#     pickle_encodings_file.close()
#
#     pickle_name_file = open(os.path.join(father_path, "faces_user.pkl"), 'wb')
#     pickle.dump(known_names, pickle_name_file)
#     pickle_name_file.close()
#     ed = time.time()
#     duration = ed - st
#     print("{:.<40}".format('[INFO] 人脸编码完成'))
#
#     # print('[INFO] 人脸信息编码完成，耗时%d秒....................' % duration)
#
#
# if __name__ == '__main__':
#     main()
