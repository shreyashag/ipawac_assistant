import cv2
import os

from assistant.plugins.utilities import paths


def face_recognizer_loop(vision_dict, faces_q, people_q):
    names = {}
    key = 0
    for (subdirs, dirs, files) in os.walk(paths.FACES_PATH):
        for subdir in dirs:
            names[key] = subdir
            key += 1
    names = names

    fischer_recognizer = cv2.face.FisherFaceRecognizer_create()
    if os.stat(paths.FACE_FISCHER_MODEL).st_size > 0:
        fischer_recognizer.read(paths.FACE_FISCHER_MODEL)
        model_loaded = 1
    else:
        model_loaded = 0

    while True:
        people = []
        faces = faces_q.get()
        if model_loaded == 1:
            if vision_dict['new_model_available'] == 1:
                vision_dict['new_model_available'] = 0
                fischer_recognizer = cv2.face.FisherFaceRecognizer_create()
                if os.stat(paths.FACE_FISCHER_MODEL).st_size > 0:
                    fischer_recognizer.read(paths.FACE_FISCHER_MODEL)
                    model_loaded = 1
                else:
                    model_loaded = 0
                # print ("NEW MODEL LOADED!")
            if vision_dict['training_started'] == 0:
                for face in faces:
                    face = cv2.equalizeHist(face)
                    confidence = fischer_recognizer.predict(face)
                    try:
                        if confidence[1] < 300:
                            person = names[confidence[0]]
                            # print ("Found {} with confidence {}".format(person, confidence[1]))
                            people.append(person)
                        people_q.put(people)
                    except BaseException:
                        pass
