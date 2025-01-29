import cv2
import tkinter as tk
from threading import Thread
import pygame
from ultralytics import YOLO

pygame.init()

face_detected_sound = pygame.mixer.Sound('/home/akz/programming/Ultra_Light_Face_Detection/face_detected.wav')

def play_face_detected_sound():
    face_detected_sound.play()

def start_face_detection(model):
    cap = cv2.VideoCapture(0)
    while detecting_faces:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                play_face_detected_sound()
        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def start_detection(model):
    global detecting_faces
    detecting_faces = True
    detection_thread = Thread(target=start_face_detection, args=(model,))
    detection_thread.start()

def stop_detection():
    global detecting_faces
    detecting_faces = False

model = YOLO('yolov8n.pt')

root = tk.Tk()
root.title("Face Detection")

start_button = tk.Button(root, text="Start Detection", command=lambda: start_detection(model))
start_button.pack(side="left", padx=10)

stop_button = tk.Button(root, text="Stop Detection", command=stop_detection)
stop_button.pack(side="left", padx=10)

root.mainloop()
