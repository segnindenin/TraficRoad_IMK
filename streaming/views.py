from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse
from streaming.camera import VideoCamera, LiveWebCam, videorecordinframe, generate, generateven, FolderCur
from django.contrib import messages

# Create your views here.
# je vais ecris un commentaire dans views.py
# bon je refaire un autre commentaire
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
import shutil

p = pyaudio.PyAudio()

def copier_fichier():
    namefile = datetime.datetime.now().strftime('%Y%m%d')
    heure = datetime.datetime.now().strftime('%H')
    v1 = int(datetime.datetime.now().strftime('%M'))-4
    v2 = int(datetime.datetime.now().strftime('%M'))-3
    v3 = int(datetime.datetime.now().strftime('%M'))-2
    v1 = f'{namefile}-{heure}{v1}.mp4'
    v2 = f'{namefile}-{heure}{v2}.mp4'
    v3 = f'{namefile}-{heure}{v3}.mp4'

    files  = [v1, v2, v3]

    for file in files:
        destination = f'DataFileSystem\\Events\\videos'
        source = f'DataFileSystem\\General\\videos\\{file}'
        if os.path.exists(source) and not os.path.exists(f'{destination}\\{file}'):
            shutil.copy2(source, destination)
        else:
            pass

def index(request):
    if request.method == "POST":
        action = request.POST.get("action")  # Récupérer la valeur de l'action du bouton
        
        if action == "action1":
            # Effectuer l'action 1
            # audio_thread = threading.Thread(target=record_audio2)
            # audio_thread.start()
            # marose = 1
            # print(marose)
            # TempEvent1 = int(datetime.datetime.now().strftime('%M'))
            record_audio2()
        time.sleep(130)
        copier_fichier()
    # copier_fichier
    return render(request, 'streaming/index.html')

def event(request):
    return render(request, 'streaming/index_event.html')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



def VideoCamera_feed(request):
    FolderCur = 'DataFileSystem\\General\\videos\\'        
    return StreamingHttpResponse(generate(VideoCamera(), FolderCur),
					content_type='multipart/x-mixed-replace; boundary=frame')

def record_audio2():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 60
    name = str(datetime.datetime.now().strftime('output_%H%M'))
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
    if request.method == "POST":
        action = request.POST.get("action")  # Récupérer la valeur de l'action du bouton
        
        if action == "action1":
            # Effectuer l'action 1
            audio_thread = threading.Thread(target=record_audio2)
            audio_thread.start()
            # record_audio2
    # FolderCur = 'DataFileSystem\\Events\\videos\\'
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