from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse
from streaming.camera import VideoCamera, LiveWebCam, videorecordinframe, generate, FolderCur
from django.contrib import messages

# Create your views here.
# je vais ecris un commentaire dans views.py
############
import cv2
import time
import os
import threading
import pyaudio
import wave
import keyboard
import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pyaudio
import wave
p = pyaudio.PyAudio()

def index(request):
	return render(request, 'streaming/index.html')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def VideoCamera_feed(request):
    if request.method == 'POST':
        return redirect('streaming/VideoCamera_Event')
    return StreamingHttpResponse(generate(VideoCamera(), FolderCur),
					content_type='multipart/x-mixed-replace; boundary=frame')

def record_audio2():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 60
    name = str(datetime.datetime.now().strftime('output_%H%M%S'))
    WAVE_OUTPUT_FILENAME = f"DataFileSystem\\Events\\phonecalls\\{name}.wav"    
    frames = []
    # if request.method == 'GET':
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
            

# FolderCur = 'DataFileSystem\\Events\\videos\\' #+ str(datetime.datetime.now().strftime('DocArchive_%Y-%m-%d'))
# FolderCur = os.path.join(os.getcwd(), str(FolderCur))
# print("ALL logs saved in dir:", FolderCur)
# if not os.path.exists(FolderCur):
#     os.mkdir(FolderCur)
# else:
#     pass
def VideoCamera_Event(request):
    if request.method == 'GET':
        audio_thread = threading.Thread(target=record_audio2)
        audio_thread.start()
        FolderCur = 'DataFileSystem\\Events\\videos\\'
        # return StreamingHttpResponse(generate(VideoCamera(), FolderCur),
		# 	        content_type='multipart/x-mixed-replace; boundary=frame')
    return StreamingHttpResponse(generate(VideoCamera(), FolderCur),
			        content_type='multipart/x-mixed-replace; boundary=frame')


def LiveWebCam_feed(request):
	return StreamingHttpResponse(generate(LiveWebCam()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def videorecordinframe_feed(request):
	return videorecordinframe()

@csrf_exempt
def record_audio(request):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 60
    WAVE_OUTPUT_FILENAME = "DataFileSystem\\Events\\phonecalls\\output2.wav"
    frames = []
    if request.method == 'GET':
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        messages.success(request, "Opération réussie !")
        callphone = True 
        context = {'callphone': callphone}
        return render(request, 'streaming/index.html')  
    # else:
    #     return HttpResponse("Error: only POST method is allowed")
