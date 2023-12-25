import cv2
import tkinter as tk
from threading import Thread
import pygame

# Initialize Pygame for sound effects
pygame.init()

# Load sound effects
face_detected_sound = pygame.mixer.Sound('/home/akz/programming/Ultra_Light_Face_Detection/face_detected.wav')  # Replace 'face_detected.wav' with your sound file

# Function to play face detected sound
def play_face_detected_sound():
    face_detected_sound.play()

# Function for face detection
def start_face_detection(face_cascade):
    # Open a connection to the camera (camera index 0 by default, you might need to change it)
    cap = cv2.VideoCapture(0)
    
    while detecting_faces:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            play_face_detected_sound()  # Play face detected sound when a face is detected

        # Display the frame with detected faces
        cv2.imshow('Face Detection', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Function to start face detection
def start_detection(face_cascade):
    global detecting_faces
    detecting_faces = True
    # Start face detection in a separate thread
    detection_thread = Thread(target=start_face_detection, args=(face_cascade,))
    detection_thread.start()

# Function to stop face detection
def stop_detection():
    global detecting_faces
    detecting_faces = False

# Load the face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create a GUI window
root = tk.Tk()
root.title("Face Detection")

# Button to start face detection
start_button = tk.Button(root, text="Start Detection", command=lambda: start_detection(face_cascade))
start_button.pack(side="left", padx=10)

# Button to stop face detection
stop_button = tk.Button(root, text="Stop Detection", command=stop_detection)
stop_button.pack(side="left", padx=10)

# Run the Tkinter main loop
root.mainloop()
