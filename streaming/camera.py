import cv2
import numpy as np
import cv2
import time
import datetime
import os

# la vie des animaux

class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)
	def __del__(self):
		self.video.release()
	def get_frame(self):
		success, image = self.video.read()
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()

class LiveWebCam(object):
	def __init__(self):
		self.url = cv2.VideoCapture(0)
	def __del__(self):
		cv2.destroyAllWindows()
	def get_frame(self):
		success,imgNp = self.url.read()
		resize = cv2.resize(imgNp, (640, 480), interpolation = cv2.INTER_LINEAR) 
		ret, jpeg = cv2.imencode('.jpg', resize)
		return jpeg.tobytes()


FolderCur = 'DataFileSystem\\General\\videos\\' + str(datetime.datetime.now().strftime('DocArchive_%Y-%m-%d'))
FolderCur = os.path.join(os.getcwd(), str(FolderCur))
print("ALL logs saved in dir:", FolderCur)
if not os.path.exists(FolderCur):
    os.mkdir(FolderCur)
else:
    pass


def generate(camera, FolderCur):
    # FolderCur = 'DataFileSystem\\General\\videos\\' + str(datetime.datetime.now().strftime('DocArchive_%Y-%m-%d'))
    # FolderCur = os.path.join(os.getcwd(), str(FolderCur))
    # print("ALL logs saved in dir:", FolderCur)
    # if not os.path.exists(FolderCur):
    #     os.mkdir(FolderCur)
    # else:
    #     pass
    namecur = datetime.datetime.now().strftime('%H-%M-%S')
    video_file_count = int((datetime.datetime.now().strftime('%H%M%S')))
    video_file = os.path.join(FolderCur, f"coupon_{namecur}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_file, fourcc, 24, (640, 480))
    start = time.time()
    video_file_count = int((datetime.datetime.now().strftime('%H%M%S')))
    out = cv2.VideoWriter(video_file, fourcc, 24, (640, 480))
    while True:
        frame = camera.get_frame()
        image = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_UNCHANGED)
        if time.time() - start > 60:
            namecur = datetime.datetime.now().strftime('%H-%M-%S')
            start = time.time()
            video_file_count += 60
            video_file = os.path.join(FolderCur, f"coupon_{namecur}.mp4")
            out = cv2.VideoWriter(video_file, fourcc, 24, (640, 480))
        out.write(image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def videorecordinframe():
    fps = 24
    video_codec = cv2.VideoWriter_fourcc("D", "I", "V", "X")
    cap = cv2.VideoCapture(0)
    ret = cap.set(3, 640)
    ret = cap.set(4, 480)
    start = time.time()
    namespecial = datetime.datetime.now().strftime('%H-%M-%S')
    video_file_count = int((datetime.datetime.now().strftime('%H%M%S')))
    video_file = os.path.join(f"coupon_{namespecial}.avi")
    print("Capture video saved location : {}".format(video_file))
    video_writer = cv2.VideoWriter(
        video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
    )
    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow("frame", frame)
            if time.time() - start > 60:
                namespecial = datetime.datetime.now().strftime('%H-%M-%S')
                start = time.time()
                video_file_count += 60
                video_file = os.path.join(f"coupon_{namespecial}.avi")
                video_writer = cv2.VideoWriter(
                    video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
                )
            video_writer.write(frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()