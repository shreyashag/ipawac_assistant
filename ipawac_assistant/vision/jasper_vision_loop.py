import cv2


def jasper_vision_loop(
    vision_dict, input_frame_q, input_gray_q,
        input_resized_gray_q, faces_rect_q, people_q):
    # cv2.namedWindow(vision_dict["main_window"], cv2.WINDOW_NORMAL)
    # cv2.namedWindow("PROCESSED", cv2.WINDOW_NORMAL)
    # cv2.namedWindow("EXTRA", cv2.WINDOW_NORMAL)

    while True:
        if vision_dict['vision_output_enabled'] == 1:
            try:
                frame_from_queue = input_frame_q.get()
                gray_from_queue = input_gray_q.get()
                resized_gray_from_queue = input_resized_gray_q.get()

                face_rects_resized = []

                image = cv2.imread(vision_dict['image_path'])

                if bool(vision_dict['message']):
                    string = (vision_dict['message'])
                    message_timeout = (vision_dict['message_timeout'])
                    cv2.putText(frame_from_queue, string, (60, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),)

                if image is not None:
                    resized_image = cv2.resize(image, (300, 300))
                    cv2.imshow("EXTRA", image)

                if vision_dict['face_detector'] == 1:
                    while not faces_rect_q.empty():
                        face_rects = faces_rect_q.get()

                    for face_rect in face_rects:
                        x = face_rect[0]
                        y = face_rect[1]
                        w = face_rect[2]
                        h = face_rect[3]
                        # print (x,y,w,h)

                        resized_width, resized_height = (112, 92)

                        x_resized = x * vision_dict['RESIZE_FACTOR']
                        y_resized = y * vision_dict['RESIZE_FACTOR']
                        w_resized = w * vision_dict['RESIZE_FACTOR']
                        h_resized = h * vision_dict['RESIZE_FACTOR']

                        resized_face_rect = [x_resized,
                                             y_resized, w_resized, h_resized]
                        face_rects_resized.append(resized_face_rect)

                    for face_rect_resized in face_rects_resized:
                        x = face_rect_resized[0]
                        y = face_rect_resized[1]
                        w = face_rect_resized[2]
                        h = face_rect_resized[3]
                        # cv2.rectangle(frame_from_queue,(x, y), (x+w, y+h), (0, 0, 255), 2)

                        if vision_dict['training_started'] == 1:
                            cv2.rectangle(
                                frame_from_queue, (x, y), (x + w, y + h), (0, 255, 255), 2)  # yellow
                            training_name = vision_dict['face_name']
                            cv2.putText(
                                frame_from_queue,
                                training_name,
                                (x,
                                 y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0,
                                 255,
                                 255),
                                2,
                                cv2.LINE_AA)
                        else:
                            cv2.rectangle(
                                frame_from_queue, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red

                    if vision_dict['face_recognizer'] == 1:
                        while not people_q.empty():
                            people = people_q.get()
                            i = 0
                            for person in people:
                                face_rect = face_rects[i]
                                face_rect_resized = face_rects_resized[i]
                                x = face_rect[0]
                                y = face_rect[1]
                                x_resized = face_rect_resized[0]
                                y_resized = face_rect_resized[1]

                                # print ("Found {} at {},{}".format(person,x_resized,y_resized))
                                # cv2.putText(resized_gray_from_queue, '%s' % (person,),  (x, y) , cv2.FONT_HERSHEY_PLAIN,2,(0, 255, 0))
                                cv2.rectangle(
                                    frame_from_queue,
                                    (x_resized,
                                     y_resized),
                                    (x_resized + w,
                                        y_resized + h),
                                    (0,
                                     255,
                                     0),
                                    3)  # green
                                cv2.putText(
                                    frame_from_queue,
                                    '%s' %
                                    (person,
                                     ),
                                    (x_resized,
                                     y_resized -
                                     5),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1,
                                    (0,
                                     255,
                                     0),
                                    1,
                                    cv2.LINE_AA)  # green

                                i = i + 1

                                # for face in face_rect_resized:
                                #     x = face [0]
                                #     y = face [1]
                                #     print (x,y)
                                #     cv2.putText(frame_from_queue, '%s' % (person,),  x-10, y-10 , cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                                # print (face_rects)
                                # cv2.putText(resized_gray_from_queue, '%s' % (person,), (face_rect[0]-10, face_rect[0]-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                                # i=i+1

                                # print ("{} at {}".format(person,face_rects[i]))
                                # for face in face_rects:
                                #     x = face[0]
                                #     y = face[1]
                                #     cv2.putText(resized_gray_from_queue, '%s' % (person,), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                                #     cv2.putText(frame_from_queue, '%s' % (person,), (x* vision_dict['RESIZE_FACTOR']-10, y* vision_dict['RESIZE_FACTOR']-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                                # i=i+1
                        #         # print ("{} at {}".format(person,face_rect))
                        #         cv2.putText(frame_from_queue, '%s' % (person,), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                        #         cv2.putText(resized_gray_from_queue, '%s' % (person,), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))

                # cv2.imshow("GRAY VISION", gray_from_queue)
                # del face_rects

                if vision_dict['training_started'] == 1:
                    training_started = "On"
                    training_name = vision_dict['face_name']
                    cv2.putText(
                        frame_from_queue,
                        "Training: " +
                        training_started +
                        " for " +
                        training_name,
                        (10,
                         25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255,
                         255,
                         255),
                        2,
                        cv2.LINE_AA)
                    if vision_dict['training_captured'] > 20:
                        vision_dict['training_captured'] = 20
                    cv2.putText(
                        frame_from_queue,
                        "Training Images captured: " +
                        str(
                            vision_dict['training_captured']) +
                        " / 20",
                        (10,
                         125),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255,
                         255,
                         255),
                        2,
                        cv2.LINE_AA)
                    cv2.putText(
                        frame_from_queue,
                        "PLEASE ENSURE THERE IS ONLY ONE SUBJECT IN THE FRAME",
                        (10,
                         100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255,
                         255,
                         255),
                        2,
                        cv2.LINE_AA)
                else:
                    training_started = "Off"
                    cv2.putText(
                        frame_from_queue,
                        "Training: " +
                        training_started,
                        (10,
                         25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255,
                         255,
                         255),
                        2,
                        cv2.LINE_AA)

                if vision_dict['face_recognizer'] == 1:
                    recognizer_started = "On"
                else:
                    recognizer_started = "Off"
                cv2.putText(
                    frame_from_queue,
                    "Recognizer: " +
                    recognizer_started,
                    (10,
                     50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,
                     255,
                     255),
                    2,
                    cv2.LINE_AA)

                if vision_dict['face_detector'] == 1:
                    detector_started = "On"
                else:
                    detector_started = "Off"
                cv2.putText(
                    frame_from_queue,
                    "Detector: " +
                    detector_started,
                    (10,
                     75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,
                     255,
                     255),
                    2,
                    cv2.LINE_AA)

                cv2.imshow("PROCESSED", frame_from_queue)

                # cv2.imshow("Resized", resized_gray_from_queue)

                cv2.waitKey(1)

            except KeyboardInterrupt:
                return
            except Exception as e:
                pass
        elif vision_dict['vision_output_enabled'] == 0:
            cv2.destroyAllWindows()
            cv2.waitKey(1)
