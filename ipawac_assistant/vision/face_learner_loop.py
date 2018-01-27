import cv2
from assistant.plugins.utilities import paths
import os
import numpy as np


def are_enough_faces():
    existingFaces = 0
    for (subdirs, dirs, files) in os.walk(paths.FACES_PATH):
        for subdir in dirs:
            # print ("Found Face in "+subdir)
            existingFaces += 1
    if existingFaces > 1:
        return True
    else:
        return False


def face_learner_loop(vision_dict, faces_q):
    fischer_recognizer = cv2.face.FisherFaceRecognizer_create()
    while True:
        if vision_dict['training_started'] == 1:
            face_name = vision_dict['face_name']
            face_path = os.path.join(paths.FACES_PATH, face_name)
            # print (face_path)
            if not os.path.isdir(face_path):
                os.makedirs(face_path)
            # print("Learning face "+ vision_dict['face_name'])

            if vision_dict['training_captured'] < vision_dict['number_of_training_images']:
                # face_resized = face from queue
                faces = faces_q.get()
                for face in faces:
                    face = cv2.equalizeHist(face)
                    l = []
                    for fn in os.listdir(face_path):
                        if str(fn[0]) != '.':  # Then is not a dot file
                            temp = (int(fn[:fn.find('.')]))
                            l.append(temp)

                    if len(l) >= 1:
                        img_no = sorted(l)[-1] + 1
                    else:
                        img_no = 1
                    if vision_dict['frame_captures'] % vision_dict['FREQ_DIV'] == 0:
                        cv2.imwrite('%s/%s.png' % (face_path, img_no), face)
                        vision_dict['training_captured'] += 1
                        # print ('Captured image: '+ str(vision_dict['training_captured'])+" at " +str(face_path))

            elif vision_dict['training_captured'] == vision_dict['number_of_training_images']:
                vision_dict['training_captured'] += 1
                # print ('Training data captured. Going to Train')
                # vision_dict['training_started'] = 0
                if are_enough_faces():
                    imgs = []
                    tags = []
                    index = 0

                    for (subdirs, dirs, files) in os.walk(paths.FACES_PATH):
                        for subdir in dirs:
                            img_path = os.path.join(
                                paths.FACES_PATH, subdir)
                            for fn in os.listdir(img_path):
                                if fn.endswith(".png"):
                                    path = img_path + '/' + fn
                                    tag = index
                                    imgs.append(cv2.imread(path, 0))
                                    tags.append(int(tag))
                            index += 1
                    (imgs, tags) = [np.array(item) for item in [imgs, tags]]
                    print("Training Facial Data")
                    fischer_recognizer.train(imgs, tags)
                    print("Saving Facial Data Model")
                    fischer_recognizer.write(paths.FACE_FISCHER_MODEL)
                    print("Training completed successfully")
                    vision_dict['training_started'] = 0
                    print("New Model Available!")
                    vision_dict['new_model_available'] = 1
                    vision_dict['training_captured'] = 0
                else:  # for if are_enough_faces()
                    print("Not enough faces to train! need atleast 2")
                    vision_dict['training_started'] = 0
                    vision_dict['training_captured'] = 0
            else:
                vision_dict['training_started'] = 0
                vision_dict['training_captured'] = 0
                # print ("TRAINING COMPLETE!")
                print(vision_dict['training_captured'])
