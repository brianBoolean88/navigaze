# 👀 Navigaze

Welcome to the **Navigaze** — a Python-based assistant that lets you control your computer using natural voice commands and your face to control your cursor! This project combines speech recognition, gaze-based cursor control, and automation to create a hands-free user experience.

![Navigaze Logo](logo.jpg)
---

## 🔧 Features

- 🎤 **Voice Recognition**: Understands natural language commands using `speech_recognition` or similar libraries.
- 🖱️ **Mouse Control**: Move the mouse cursor using gaze or directional commands.
- 📄 **Typing**: Dictate text to be typed automatically.
- 🌐 **Browser and Window Navigation**: Switch tabs/windows and control browser behavior.
- 🔍 **Scrolling & Clicking**: Scroll through pages and click with voice commands.
- 🚫 **Pause, Resume, or Stop**: Full control over when the assistant listens or acts.

---

## 📋 List of Voice Commands

Here are some example commands you can use:

| Command            | Description                             |
|--------------------|-----------------------------------------|
| `confirm`          | Left mouse click                        |
| `continue`         | Start gaze tracking                     |
| `pause`            | Pause gaze tracking                     |
| `end all`          | Terminate the assistant                 |
| `up`, `down`       | Move cursor in direction                |
| `move up`          | Same as `up` (natural phrasing)         |
| `switch window`    | Alt + Tab window switcher               |
| `press tab`        | Press the Tab key                       |
| `choose window`    | Finalize selected window (Alt Up)       |
| `switch chrome`    | Switch browser tab (Ctrl + Tab)         |
| `type hello world` | Types `hello world`                     |
| `enter`            | Press Enter                             |
| `open youtube`     | Opens YouTube in browser                |
| `reset`            | Centers the mouse cursor                |
| `close`            | Closes current tab/window               |
| `scroll up`        | Scrolls page up                         |
| `scroll down`      | Scrolls page down                       |

---

## 🖥️ Requirements

Mobile webcam
Install the following Python packages:

```bash
pip install opencv-python mediapipe pyautogui SpeechRecognition pyttsx3 pywinauto
