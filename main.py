import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import threading
import time
import sys
import webbrowser
import pyttsx3
from pywinauto import Desktop

screen_w, screen_h = pyautogui.size()
move_cursor = True
end_sys = False
alt_held = False

pyautogui.FAILSAFE = False

def choose_webcam(max_tested=5):
    print("Available webcams:\n")
    available = []

    for i in range(max_tested):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"[{i}] Webcam {i} - Working")
            available.append(i)
            cap.release()
        else:
            print(f"[{i}] Webcam {i} - Not detected")

    if not available:
        print("❌ No webcams found.")
        sys.exit()

    while True:
        try:
            choice = int(input("\nEnter the number of the webcam you want to use: "))
            if choice in available:
                print(f"✅ Selected webcam: {choice}")
                return choice
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def choose_mic():
    mic_list = sr.Microphone.list_microphone_names()
    print("Available microphones:\n")

    for i, mic in enumerate(mic_list):
        print(f"[{i}] {mic}")

    while True:
        try:
            choice = int(
                input("\nEnter the number of the microphone you want to use: "))
            if 0 <= choice < len(mic_list):
                print(f"Selected microphone: {mic_list[choice]}")
                return choice
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")


def move_cursor_func(direction, pixels=30):
    screen_w, screen_h = pyautogui.size()
    current_x, current_y = pyautogui.position()

    if direction == "left":
        new_x = max(current_x - pixels, 0)
        new_y = current_y
    elif direction == "right":
        new_x = min(current_x + pixels, screen_w - 1)
        new_y = current_y
    elif direction == "up":
        new_x = current_x
        new_y = max(current_y - pixels, 0)
    elif direction == "down":
        new_x = current_x
        new_y = min(current_y + pixels, screen_h - 1)
    else:
        return

    pyautogui.moveTo(new_x, new_y)


def switch_to_window(index):
    windows = Desktop(backend="uia").windows()
    windows = [w for w in windows if w.is_visible()
                                                  and w.window_text().strip()]

    if 0 <= index < len(windows):
        window = windows[index]
        try:
            window.set_focus()
            say(f"Switched to window {index}: {window.window_text()}")
        except Exception as e:
            say(f"Failed to switch window: {str(e)}")
    else:
        say(f"Invalid window index: {index}")


engine = pyttsx3.init()


def say(text):
    print(text)
    threading.Thread(target=_speak, args=(text,), daemon=True).start()


def _speak(text):
    engine.say(text)
    engine.runAndWait()


class VoiceController:
    def __init__(self, mic_index=0):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(device_index=mic_index)
        self.listening = True

    def listen_loop(self):
        global move_cursor, end_sys, screen_w, screen_h, alt_held
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)

            while self.listening:
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    command = self.recognizer.recognize_google(audio).lower()
                    # say(f"Heard: {command}")

                    if "confirm" in command:
                        pyautogui.click()
                        say("Triggering click!")
                    elif "continue" in command:
                        move_cursor = True
                        say("Starting gaze direction")
                    elif "pause" in command:
                        move_cursor = False
                        say("Stopping gaze direction")
                    elif "end all" in command:
                        print("Stopping all processes")
                        engine.say("Stopping all processes")
                        engine.runAndWait()

                        end_sys = True
                        sys.exit()
                        quit()
                    elif command in ["up", "down", "left", "right"]:
                        move_cursor_func(command)
                    elif command in ["move up", "move down", "move left", "move right"]:
                        move_cursor_func(command[5:])
                    elif "switch window" in command:
                        say("say press tab or choose window")
                        pyautogui.keyDown("alt")
                        pyautogui.press("tab")
                    elif "press tab" in command:
                        pyautogui.press("tab")
                    elif "choose window" in command:
                        pyautogui.keyUp("alt")
                    elif "switch chrome" in command:
                        pyautogui.keyDown("ctrl")
                        pyautogui.press("tab")
                        pyautogui.keyUp("ctrl")
                        say("🔀 Switching to next tab...")
                    elif command.startswith("type "):
                        to_type = command[5:]  # Get everything after "type "
                        # You can adjust the speed with 'interval
                        pyautogui.write(to_type, interval=0.05)
                        say("Typing")
                    elif "enter" in command:
                        pyautogui.press("enter")
                        say("🚀Pressing Enter")
                    elif "open youtube" in command:
                        webbrowser.open("https://www.youtube.com/")
                    elif "reset" in command:
                        pyautogui.moveTo(screen_w // 2, screen_h // 2)
                    elif "close" in command:
                        pyautogui.keyDown("ctrl")
                        pyautogui.press("w")
                        pyautogui.keyUp("ctrl")
                        say("closing window")
                    elif "scroll up" in command:
                        pyautogui.scroll(500)  # Scrolls up
                        say("Scrolling up")
                    elif "scroll down" in command:
                        pyautogui.scroll(-500)  # Scrolls down
                        say("Scrolling down")
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    #say("Didn't catch that.")
                    continue
                except sr.RequestError as e:
                    #say(f"API error: {e}")
                    continue

class NaviGaze:
    global screen_h, screen_w, end_sys
    def __init__(self, cam_index):
        # SETTINGS
        self.last_nose_ref = None
        self.threshold = 0.005
        self.last_x_dir = None
        self.last_y_dir = None

        # Video Capture
        self.cap = cv2.VideoCapture(cam_index)
        if not self.cap.isOpened():
            say("❌ Cannot access webcam.")
            exit()

        # Facial Recognition
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(
            thickness=1, circle_radius=1, color=(0, 255, 0))  # green

    def run(self):
        while True:

            ret, self.frame = self.cap.read()
            if not ret:
                say("❌ Enable permissions and restart.")
                break

            # Normalize
            self.frame = cv2.flip(self.frame, 1)
            rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

            # Eye recognition
            result = self.face_mesh.process(rgb)

            if result.multi_face_landmarks:
                for face_landmarks in result.multi_face_landmarks:
                    # Drawing segment for debugging
                    self.mp_drawing.draw_landmarks(
                        image=self.frame,
                        landmark_list=face_landmarks,
                        connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=self.drawing_spec
                    )

                    h, w, _ = self.frame.shape
                    eye_indices = [33, 133, 160, 159, 158, 157, 173,
                                362, 263, 387, 386, 385, 384, 398]

                    for idx in eye_indices:
                        lm = face_landmarks.landmark[idx]
                        x, y = int(lm.x * w), int(lm.y * h)
                        cv2.circle(self.frame, (x, y), 2, (255, 0, 0), -1)

                    # Mapping to screen
                    # Left iris: 469-473
                    # Right iris: 474-478
                    # Nose: 1

                    detection = face_landmarks.landmark[1]
                    x_normalized = detection.x
                    y_normalized = detection.y

                    self.mapToScreen(x_normalized, y_normalized)
                    #self.findDir(x_normalized, y_normalized)

            # Display
            cv2.imshow("Eye track", self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or end_sys:
                self.cap.release()
                cv2.destroyAllWindows()
                break
    
    def mapToScreen(self, x, y):

        if self.last_nose_ref == None:
            self.last_nose_ref = (x, y)
            return
        
        dx = abs(x - self.last_nose_ref[0])
        dy = abs(y - self.last_nose_ref[1])

        frame_h, frame_w, _ = self.frame.shape
        min_x, max_x = 0.45, 0.55
        min_y, max_y = 0.45, 0.55

        pt1 = (int(min_x * frame_w), int(min_y * frame_h))  # Top-left corner
        pt2 = (int(max_x * frame_w), int(max_y * frame_h))  # Bottom-right corner

        cv2.rectangle(self.frame, pt1, pt2, (0, 255, 255), 2)  # Yellow box
        cv2.putText(self.frame, "Tracking Box", (pt1[0], pt1[1] - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        if (dx <= self.threshold and dy <= self.threshold) or move_cursor == False:
            return

        self.last_nose_ref = (x, y)

        percent_x = min(1, max(0, (x - min_x) / (max_x - min_x)))
        percent_y = min(1, max(0, (y - min_y) / (max_y - min_y)))

        actual_x = int(percent_x * screen_w)
        actual_y = int(percent_y * screen_h)

        pyautogui.moveTo(actual_x, actual_y)

        print(f"Looking at screen coordinates: ({percent_x}, {percent_y})")

        

    def findDir(self, x, y):
        if self.last_nose_ref == None:
            self.last_nose_ref = (x, y)
            return

        dx = x - self.last_nose_ref[0]
        dy = y - self.last_nose_ref[1]

        #say(dx, dy)

        x_dir = None
        y_dir = None

        if dx > self.threshold:
            x_dir = "right"
        elif dx < -self.threshold:
            x_dir = "left"

        if dy > self.threshold:
            y_dir = "down"
        elif dy < -self.threshold:
            y_dir = "up"

        #if x_dir:
            #say(f"Nose moved in the x direction: {x_dir}")

        #if y_dir:
            #say(f"Nose moved in the y direction: {y_dir}")

        self.last_nose_ref = (x, y)
        self.last_x_dir = x_dir
        self.last_y_dir = y_dir
        move_cursor_func(x_dir, screen_h/5)
        move_cursor_func(y_dir, screen_w/5)
    


if __name__ == "__main__":
    mic_index = choose_mic()
    webcam_index = choose_webcam()

    voice = VoiceController(mic_index=mic_index)
    threading.Thread(target=voice.listen_loop, daemon=True).start()

    tracker = NaviGaze(cam_index=webcam_index)
    tracker.run()