import os
import cv2
import numpy as np
import time
from . import jasperpath
import multiprocessing
# import Queue


class myOpenVision():

    def __init__(self, src=0):

        self.FREQ_DIV = 4  # frequency divider for capturing training images
        self.number_of_training_images = int(20)
        self.RESIZE_FACTOR = 4
        self.src = src
        self.vision_enabled = True
        self.WINDOW_NAME = "Jasper-Vision"

        self.main_window = cv2.namedWindow(self.WINDOW_NAME)
        self.image_location = ''

        self.face_dir = jasperpath.FACES_PATH

        # self.model = cv2.face.createFisherFaceRecognizer()
        self.count_captures = 0
        self.count_timer = 0

        # self.stream = cv2.VideoCapture(self.src)
        # (self.grabbed, self.frame) = self.stream.read()
        # self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        self.image_path = ''
        self.training_complete = 0
        self.training_started = 0

        # self.faceDectectorThread = threading.Thread(
        #     target=self.faceDectector, args=())

        self.faceName = ''
        self.face_path = ''

        # self.faceLearnerThread = threading.Thread(
        #     target=self.learnFaceThread, args=(self.faceName,))
        # self.faceLearnerThread.start()

        self.front_faces = ''
        self.right_faces = ''
        self.front_faces_draw = ''

        self.ui_running = 0
        self.face_recognizer = 0
        self.person = ''
        # self.faceRecognizerThread = threading.Thread(
        #     target=self.faceThread, args=())
        # self.faceRecognizerThread.start()
        self.recognized_faces = []

    # def startVision(self):
    #   self.vision_enabled = True
    #   try:
    #     self.producerThread.start()
    #   except:
    #     print ("Error: unable to start thread")
    #   return

    def showFrameOutput(self, frame_from_q):
        if (self.grabbed):
            frame = frame_from_q

        # for (x, y, w, h) in self.front_faces_draw:
        #   face = self.gray[y:y + h, x:x + w]
        #   resized_width, resized_height = (112, 92)
        #   face_resized = cv2.resize(face, (resized_width, resized_height))
        #   cv2.rectangle(processed_frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        #   face_resized = cv2.equalizeHist(face_resized)
        #   if self.face_recognizer == 1:
        #     self.recognized_faces = []
        #     confidence = self.model.predict(face_resized)
        #     if confidence[1] < 500:
        #       person = self.names[confidence[0]]
        #       self.recognized_faces.append(person)
        #       cv2.rectangle(processed_frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
        #       cv2.putText(processed_frame, '%s - %.0f' % (person, confidence[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
        #     else:
        #       person = 'Unknown'
        #       cv2.putText(processed_frame, self.person, (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
        #       # print person

        #       cv2.rectangle(self.frame, (x,y), (x+w, y+h), (0, 0, 255), 3)

        #   if self.training_started == 1:
        #     cv2.putText(
        #         processed_frame,
        #         self.faceName,
        #         (x - 10, y - 10),
        #         cv2.FONT_HERSHEY_PLAIN,
        #         1,
        #         (0, 255, 0),)

        # for (x, y, w, h) in self.right_faces:
        #   cv2.rectangle(processed_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # the_q.put(processed_frame)
        cv2.imshow(self.WINDOW_NAME, frame)
        return

    def drawUI(self, frame_q):
        self.ui_running = 1
        while True:
            #   cv2.putText(self.frame,"Training On",(10, 20),cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0),)
            #   cv2.putText(self.frame,'Captured training images:' + str(self.count_captures),(10, 50),cv2.FONT_HERSHEY_PLAIN,
            #       1,(0, 255, 255),)
            # else:
            #   cv2.putText(self.frame,"Training Off",(10, 20),cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0),)
            try:
                frame = frame_q.get()
                cv2.imshow(self.WINDOW_NAME, frame)
                cv2.waitKey(1)
                # if self.training_started == 1:

                # cv2.waitKey(1)
                # self.showFrameOutput(frame)
                # if len(self.recognized_faces) > 0:
                #   for face in self.recognized_faces:
                #     if len(self.recognized_faces) > 0:
                #       # print ("Found face {}".format(face))
                #       pass
            except KeyboardInterrupt:
                self.stopVision()
                break
        return

    def producer(self, frame_q):
        while True:
            # stream = cv2.VideoCapture(0)
            print("HERE NOW")
            # grabbed, frame = stream.read()
            if frame is not None:
                self.count_timer += 1
                # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # gray_resized = cv2.resize(
                # gray, (int(gray.shape[1]/self.RESIZE_FACTOR),
                # int(gray.shape[0]/self.RESIZE_FACTOR)))

                frame_q.put(frame)
                # gray_q.put(gray)
                # gray_resized_q.put(gray_resized)

    def stopVision(self):
        # self.vision_enabled=False
        # cv2.imshow(self.WINDOW_NAME, self.default_image)
        self.ui_running = 0
        cv2.destroyAllWindows()
        cv2.waitKey(2)
        return

    def faceRecognizer(self):
        names = {}
        key = 0
        for (subdirs, dirs, files) in os.walk(self.face_dir):
            for subdir in dirs:
                # print subdir
                names[key] = subdir
                key += 1
                # print names[key]
        # print key
        self.names = names
        print(self.names)
        # print ("Loading data from {}".format(self.face_dir))
        # print ("Loading model from {}").format(jasperpath.FACE_FISCHER_MODEL)
        self.model.load(jasperpath.FACE_FISCHER_MODEL)

        self.face_recognizer = 1

    def faceThread(self):
        while True:
            if self.face_recognizer == 1:
                self.recognized_faces = []
                recognized_faces = []
                if len(self.front_faces) > 0:
                    areas = []
                    for (x, y, w, h) in self.front_faces:
                        areas.append(w * h)
                    (max_area, idx) = max([(val, idx) for (idx, val) in
                                           enumerate(areas)])

                    face_sel = self.front_faces[idx]

                    x = face_sel[0] * self.RESIZE_FACTOR
                    y = face_sel[1] * self.RESIZE_FACTOR
                    w = face_sel[2] * self.RESIZE_FACTOR
                    h = face_sel[3] * self.RESIZE_FACTOR
                    face = self.gray[y:y + h, x:x + w]
                    resized_width, resized_height = (112, 92)
                    face_resized = cv2.resize(
                        face, (resized_width, resized_height))
                    face_resized = cv2.equalizeHist(face_resized)
                    confidence = self.model.predict(face_resized)
                    if confidence[1] < 100:
                        # print person
                        # cv2.rectangle(self.frame, (x,y), (x+w, y+h), (255, 0, 0), 3)
                        # cv2.putText(self.frame, '%s - %.0f' % (person, confidence[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                        person = self.names[confidence[0]]
                        recognized_faces.append(person)
                        self.person = person
                    else:
                        person = 'Unknown'
                        # print person
                        self.person = person
                        # cv2.rectangle(self.frame, (x,y), (x+w, y+h), (0, 0, 255), 3)
                        # cv2.putText(self.frame, person, (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                    if len(self.recognized_faces) > 0:
                        for face in self.recognized_faces:
                            pass
                            # print face
                            # print ("Found face {}".format(face))
                    self.recognized_faces = recognized_faces

    def faceDectector(self):
        while True:
            self.front_faces_draw = self.front_face_cascade.detectMultiScale(
                self.gray,
                scaleFactor=1.1,
                minNeighbors=7,
                minSize=(50, 50),
                flags=cv2.CASCADE_SCALE_IMAGE)
            self.front_faces = self.front_face_cascade.detectMultiScale(
                self.gray_resized,
                scaleFactor=1.1,
                minNeighbors=7,
                minSize=(50, 50),
                flags=cv2.CASCADE_SCALE_IMAGE)
            self.right_faces = self.right_face_cascade.detectMultiScale(
                self.gray_resized,
                scaleFactor=1.1,
                minNeighbors=7,
                minSize=(50, 50),
                flags=cv2.CASCADE_SCALE_IMAGE)

    def startFaceDetection(self):
        self.faceDectectorThread.start()

    def process_image(self, inImg):
        frame = cv2.flip(inImg, 1)
        return frame

    def learnFace(self, faceName):
        self.faceName = faceName
        self.face_path = os.path.join(self.face_dir, self.faceName)
        print(self.face_path)
        if not os.path.isdir(self.face_path):
            os.makedirs(self.face_path)
        self.stopVision()
        self.training_started = 1
        # time.sleep(2)
        self.drawUI()

    def learnFaceThread(self, faceName):
        self.training_complete = 0
        self.count_captures = 0
        # while (self.training_complete ==0 ):
        while True:
            if self.training_started == 1:
                print("Learning face " + faceName)
                if self.count_captures < self.number_of_training_images:

                    inImg = np.array(self.frame)
                    face_path = self.face_path

                    # outImg = self.process_image(inImg,faceName)
                    outImg = self.process_image(inImg)

                    if len(self.front_faces) > 0:
                        areas = []
                        for (x, y, w, h) in self.front_faces:
                            areas.append(w * h)
                        (max_area, idx) = max([(val, idx) for (idx, val) in
                                               enumerate(areas)])

                        face_sel = self.front_faces[idx]

                        x = face_sel[0] * self.RESIZE_FACTOR
                        y = face_sel[1] * self.RESIZE_FACTOR
                        w = face_sel[2] * self.RESIZE_FACTOR
                        h = face_sel[3] * self.RESIZE_FACTOR

                        face = self.gray[y:y + h, x:x + w]

                        resized_width, resized_height = (112, 92)

                        face_resized = cv2.resize(
                            face, (resized_width, resized_height))

                        img_no = sorted([int(fn[:fn.find('.')]) for fn in
                                         os.listdir(face_path) if fn[0] != '.']
                                        + [0])[-1] + 1

                        if self.count_timer % self.FREQ_DIV == 0:
                            # print face
                            # cv2.imwrite('%s/face-%s.png' % (face_path, img_no),face)
                            # cv2.imwrite('%s/selfgray-%s.png' % (face_path, img_no),self.gray)
                            # print ('%s/%s.png' % (face_path, img_no))

                            face = self.gray[y:y + h, x:x + w]
                            face_resized = cv2.resize(
                                face, (resized_width, resized_height))
                            face_resized = cv2.equalizeHist(face_resized)
                            cv2.imwrite(
                                '%s/%s.png' %
                                (face_path, img_no), face_resized)
                            self.count_captures += 1
                            print('Captured image: ' + self.count_captures)
                            time.sleep(1)

                elif self.count_captures == self.number_of_training_images:
                    self.count_captures += 1
                    self.count_captures = 0
                    print('Training data captured. Going to Train')
                    self.training_complete = 1
                    self.training_started = 0

                    if self.are_enough_faces():
                        imgs = []
                        tags = []
                        index = 0

                        for (subdirs, dirs, files) in os.walk(self.face_dir):
                            for subdir in dirs:
                                img_path = os.path.join(self.face_dir, subdir)
                                for fn in os.listdir(img_path):
                                    if fn.endswith(".png"):

                                        path = img_path + '/' + fn
                                        tag = index
                                        imgs.append(cv2.imread(path, 0))
                                        tags.append(int(tag))
                                index += 1
                        (imgs, tags) = [np.array(item)
                                        for item in [imgs, tags]]
                        print("Training Facial Data")
                        self.model.train(imgs, tags)
                        print("Saving Facial Data Model")
                        self.model.save(jasperpath.FACE_FISCHER_MODEL)
                        print("Training completed successfully")
                        self.face_recognizer = 1
                    else:
                        print("Not enough faces to train! need atleast 2")

                #     cv2.putText(
                #         self.frame,
                #         str('Training complete, press q to exit'),
                #         (20, 20),
                #         cv2.FONT_HERSHEY_PLAIN,
                #         2,
                #         (0, 255, 255),
                #         )

    def load_trained_data(self):
        names = {}
        key = 0
        for (subdirs, dirs, files) in os.walk(self.face_dir):
            for subdir in dirs:
                names[key] = subdir
                key += 1
        print(key)
        self.names = names
        print("Loading data from {}".format(self.face_dir))
        self.model.load('fisher_trained_data.xml')

    def get_image(self):
        ret, self.frame = self.video_source.read()
        inImg = np.array(self.frame)
        # self.outImg = self.process_image(inImg)

    def fisher_train_data(self):
        imgs = []
        tags = []
        index = 0
        print("Creating model to train")
        for (subdirs, dirs, files) in os.walk(self.face_dir):
            for subdir in dirs:
                img_path = os.path.join(self.face_dir, subdir)
                # print img_path
                for fn in os.listdir(img_path):
                    if fn.endswith(".png"):
                        path = img_path + '/' + fn
                        # print imgpath
                        # time.sleep(0.2)
                        tag = index
                        # print index
                        print("appending image to imgs")
                        # print (cv2.imread(imgpath, 0))
                        imgs.append(cv2.imread(path, 0))
                        tags.append(int(tag))
                index += 1

        (imgs, tags) = [np.array(item) for item in [imgs, tags]]
        print("Training Facial Data")
        self.model.train(myimgs, mytags)
        print("Saving Facial Data Model")
        print(jasperpath.FACE_FISCHER_MODEL)
        self.model.save(jasperpath.FACE_FISCHER_MODEL)
        print("Training completed successfully")
        return

    def are_enough_faces(self):
        existingFaces = 0
        for (subdirs, dirs, files) in os.walk(self.face_dir):
            for subdir in dirs:
                print("Found Face in" + subdir)
                existingFaces += 1

        # if existingFaces==1:
            # print "Found only one face, need atleast one more face for training to work"
            # mic.say("What is the name of the person whose face you want to learn?")
            # person_name2=mic.activeListen()
            # mic.say("How many training images do you want to capture?")
            # number_of_training_images2=mic.activeListen()

            # trainer2 = TrainFisherFaces(person_name2, number_of_training_images2)
            # trainer2.capture_training_images()

            # if trainer2.are_enough_faces(mic):
            #     trainer2.fisher_train_data()
            #     trainer2.delete()

        if existingFaces > 1:
            print("found faces, going to train")
            return True
        else:
            print("found no faces")
            return False


def programLoop():
    while True:
        input_command = raw_input()
    #   # print input_command
        if (input_command == "startVision"):
            myVision.startVision()
        if (input_command == "drawUI"):
            myVision.drawUI()
        if input_command == 'faceDetectorOn':
            myVision.startFaceDetection()
        if input_command == 'faceDetectorOff':
            myVision.stopFaceDetection()
        if input_command == 'getFaces':
            # print "from program Loop"
            print(myVision.recognized_faces)
            print("Faces Sent")
        if input_command == 'faceRecognizerOn':
            myVision.faceRecognizer()
        if input_command == 'learnFace':
            myVision.face_recognizer = 0
            name_command = raw_input()
            print("Learning face" + name_command)
            myVision.learnFace(name_command)
            myVision.face_recognizer = 1


def myVision1_producer(frame_q):
    count_timer = 0
    stream = cv2.VideoCapture(0)
    while True:
        _, img = cap.read()
        if img is not None:
            the_q.put(img)
    # while True:
    #   # stream = cv2.VideoCapture(0)
    #   print ("HERE NOW")
        # frame = None
        # # grabbed, frame = stream.read()
        # if frame is not None:
        #   count_timer += 1
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray_resized = cv2.resize(
        # gray, (int(gray.shape[1]/self.RESIZE_FACTOR),
        # int(gray.shape[0]/self.RESIZE_FACTOR)))

        # frame_q.put(frame)
        # gray_q.put(gray)
        # gray_resized_q.put(gray_resized)


def cam_loop(the_q):
    cap = cv2.VideoCapture(0)

    while True:
        _, img = cap.read()
        if img is not None:
            the_q.put(img)


def show_loop(the_q):
    # cv2.setNumThreads(-1)
    cv2.namedWindow('pepe')

    while True:
        from_queue = the_q.get()
        cv2.imshow('pepe', from_queue)
        cv2.waitKey(1)


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(multiprocessing.SUBDEBUG)
    frame_q = multiprocessing.Queue(1)
    gray_q = multiprocessing.Queue(1)
    gray_resized_q = multiprocessing.Queue(1)
    # myVision1 = myOpenVision()
    # myVision1.vision_enabled= True
    # myVision1.producer(frame_q,gray_q,gray_resized_q)
    # producer_process = multiprocessing.Process(target=myVision1.producer,args=(frame_q,gray_q,gray_resized_q))

    # producer_process = multiprocessing.Process(target=myVision1_producer,args=(frame_q,))
    cam_process = multiprocessing.Process(target=cam_loop, args=(frame_q, ))
    show_process = multiprocessing.Process(target=show_loop, args=(frame_q, ))
    cam_process.start()
    # visionProcess = multiprocessing.Process(target=myVision.drawUI,args=(frame_q,))
    show_process.start()

    print("HERE")
    i = 0
    while True:
        i = i + 1

    # myVision1_producer(frame_q)

    producer_process.start()
    # visionProcess.start()

    # myVision.startVision()
    # myVision.startFaceDetection()
    # myVision.faceRecognizer()
    # myVision.drawUI()
    # programLoop()
