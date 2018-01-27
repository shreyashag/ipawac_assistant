import cv2


def gray_resizing_loop(vision_dict, gray_q, output_gray_resized_q):
    while True:
        gray_frame = gray_q.get()
        gray_q.put(gray_frame)
        gray_resized = cv2.resize(gray_frame,
                                  (int(gray_frame.shape[1] / vision_dict["RESIZE_FACTOR"]),
                                   int(gray_frame.shape[0] / vision_dict["RESIZE_FACTOR"])))
        output_gray_resized_q.put(gray_resized)
