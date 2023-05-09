#
# -*-------------coding=utf-8-----------------*-
'''
/* demo_sken.py      4月 2023 15:57   
*---------------------------------------------*
*     Project Name : background_management_system          
*                                             
*     File Name    : demo_sken.py                  
*                                             
*     Programmer   : yufanyi@hust.edu.cn                  
*                                             
*     Start Date   : 04/16/2023  
*                                             
*     Last Update  : 04/16/2023 
*                                             
*---------------------------------------------*
*   代码描述:                                   
*   
*---------------------------------------------*
'''

import mediapipe as mp
import sys, cv2
import numpy as np

# from apps.training.models import *

from apps.training.models import KeyFrame


def skeleton_tran(skeleton, norm=False):
    # blazepose 33-> 15

    n = [-1, 24, 26, 28,
         23, 25, 27,
         12, 14, 16,
         11, 13, 15,
         -1, 0]

    skeleton_ = np.zeros((15, 3))
    for i in range(3):
        skeleton_[0][i] = (skeleton[23][i] + skeleton[24][i]) / 2
        skeleton_[13][i] = (skeleton[11][i] + skeleton[12][i]) / 2
    for i in range(15):
        if n[i] != -1:
            skeleton_[i] = skeleton[n[i]]
    if norm:
        a = skeleton_[0].copy()
        for i in range(15):
            skeleton_[i] -= a
    return skeleton_


def keyframe_extract(skeleton_list, visibility=0.8, movements=0.09):
    # skeleton_list: [frames, key-points, coordinates], coordinates [x, y, z, visibility(optional)]
    # visibility: threshold
    # movements: threshold
    skeleton_list = np.asarray(skeleton_list)
    frames = skeleton_list.shape[0]
    kps = skeleton_list.shape[1]
    visib = skeleton_list.shape[2]

    key_frames = []
    skeleton_filter_list = []

    for frame in range(frames - 2):
        skeleton_i = skeleton_list[frame]
        skeleton_ii = skeleton_list[frame + 1]
        # skeleton_iii = skeleton_list[frame + 2]

        diff = np.ones([kps, 2])
        diff[:, 0] = np.linalg.norm((skeleton_i[:, 0:3] - skeleton_ii[:, 0:3]), axis=1)
        if visib == 4:
            diff[:, 1] = skeleton_i[:, 3] * skeleton_ii[:, 3]

        # move_flag = 0

        for idx in range(kps):
            if diff[idx, 1] > visibility:
                if diff[idx, 0] > movements:
                    # move_flag = 1
                    key_frames.append(frame)
                    skeleton_filter_list.append(skeleton_i)
                    break
        if frame == 0:
            key_frames.append(frame)
            skeleton_filter_list.append(skeleton_i)

    return key_frames, skeleton_filter_list


def get_keyFrame(video_path):
    skeleton_list = []
    cap = cv2.VideoCapture(video_path)
    import os
    success, img = cap.read()
    skeleton = np.zeros((33, 3))
    pose = mp.solutions.pose.Pose(static_image_mode=False,
                                  model_complexity=0,
                                  smooth_landmarks=True,
                                  enable_segmentation=True,
                                  min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)
    while success:
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_RGB)
        if results.pose_world_landmarks:
            for i in range(33):
                skeleton[i][0] = results.pose_world_landmarks.landmark[i].x
                skeleton[i][1] = results.pose_world_landmarks.landmark[i].y
                skeleton[i][2] = results.pose_world_landmarks.landmark[i].z

        skeleton_list.append(skeleton_tran(skeleton))
        success, img = cap.read()

    return keyframe_extract(skeleton_list)


def create_keyframe(chapter_id, path):
    frame, skeleton = get_keyFrame(path)
    # print(frame, skeleton)
    keyframe_time = frame[0]
    keyframe_Skeleton = skeleton[0].tobytes()
    time_skeleton = zip(frame, skeleton)
    keyframes = []
    for item in time_skeleton:
        keyframe = KeyFrame(chapter_id=chapter_id, keyframe_time=item[0], keyframe_Skeleton=item[1].tobytes())
        keyframes.append(keyframe)
    KeyFrame.objects.bulk_create(keyframes)


if __name__ == '__main__':
    create_keyframe()
