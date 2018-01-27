import cv2

from assistant.plugins.utilities import paths


def face_detector_loop(
        vision_dict,
        input_gray_q,
        input_gray_resized_q,
        faces_rect_q,
        faces_q):
    while True:
        front_face_cascade = cv2.CascadeClassifier(
            paths.FRONT_CASCADE_PATH)
        right_face_cascade = cv2.CascadeClassifier(
            paths.RIGHT_LPB_CASCADE_PATH)
        try:
            if vision_dict['face_detector'] == 1:
                face_rects = []
                face_resized_list = []
                gray_from_queue = input_gray_q.get()
                gray_resized_from_queue = input_gray_resized_q.get()

                input_gray_q.put(gray_from_queue)
                input_gray_resized_q.put(gray_resized_from_queue)

                front_faces = front_face_cascade.detectMultiScale(
                    gray_resized_from_queue,
                    scaleFactor=1.1,
                    minNeighbors=7,
                    minSize=(50, 50),
                    flags=cv2.CASCADE_SCALE_IMAGE)
                # right_faces = right_face_cascade.detectMultiScale(
                #   gray_resized_from_queue,
                #   scaleFactor=1.1,
                #   minNeighbors=7,
                #   minSize=(50, 50),
                #   flags=cv2.CASCADE_SCALE_IMAGE)
                for (x, y, w, h) in front_faces:
                    face_rect = [x, y, w, h]
                    face = gray_resized_from_queue[y:y + h, x:x + w]

                    face_rects.append(face_rect)
                    resized_width, resized_height = (112, 92)
                    face_resized = cv2.resize(
                        face, (resized_width, resized_height))
                    face_resized_list.append(face_resized)

                faces_q.put(face_resized_list)
                faces_rect_q.put(face_rects)

        except KeyboardInterrupt:
            return
        except queue.Empty as e:
            pass
        except queue.Full as e:
            pass
