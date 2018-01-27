import queue
import cv2


def camera_loop(vision_dict, producer_frame_q, producer_gray_q):
    cap = cv2.VideoCapture(vision_dict["src"])
    while True:
        if cap:
            try:
                ret, frame = cap.read()
                if frame is not None:
                    producer_frame_q.put(frame)
                    vision_dict['frame_captures'] += 1
                    # self.count_timer += 1
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    producer_gray_q.put(gray)
            except KeyboardInterrupt:
                return
            except queue.Full:
                pass
