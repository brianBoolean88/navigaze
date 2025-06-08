# 🎙️ Voice Command Reference

This document describes all the available voice commands and their effects in your Python automation assistant.

---

## 🔘 `confirm`
- **Action**: Performs a left mouse click at the current cursor position.
- **Use Case**: Simulates confirming or selecting an item.
- **Implementation**: `pyautogui.click()`

---

## ▶️ `continue`
- **Action**: Starts gaze tracking and cursor control.
- **Effect**: Sets `move_cursor = True`
- **Spoken Feedback**: "Starting gaze direction"

---

## ⏸️ `pause`
- **Action**: Pauses gaze tracking and cursor control.
- **Effect**: Sets `move_cursor = False`
- **Spoken Feedback**: "Stopping gaze direction"

---

## 🛑 `end all`
- **Action**: Terminates all running processes and exits the program.
- **Effect**:
  - Announces shutdown
  - Sets `end_sys = True`
  - Executes `sys.exit()` and `quit()`

---

## ⬆️⬇️⬅️➡️ `up`, `down`, `left`, `right`
- **Action**: Moves the cursor in the specified direction.
- **Implementation**: `move_cursor_func(direction)`

---

## 🔄 `move up`, `move down`, `move left`, `move right`
- **Action**: Same as above, supports commands prefixed with `"move "`.
- **Implementation**: `move_cursor_func(command[5:])`

---

## 🪟 `switch window`
- **Action**: Activates `Alt + Tab` to switch windows.
- **Steps**:
  - Holds `Alt`
  - Presses `Tab`
- **Spoken Feedback**: "say press tab or choose window"

---

## ↹ `press tab`
- **Action**: Sends a `Tab` keystroke to cycle through open windows or tabs.

---

## ✅ `choose window`
- **Action**: Releases the `Alt` key to finalize window switch selection.

---

## 🌐 `switch chrome`
- **Action**: Switches to the next tab in Google Chrome.
- **Steps**:
  - Holds `Ctrl`
  - Presses `Tab`
  - Releases `Ctrl`
- **Spoken Feedback**: "🔀 Switching to next tab..."

---

## ⌨️ `type [text]`
- **Action**: Types the text that follows the word `type`.
- **Example**: `type hello world` types “hello world”.
- **Implementation**: `pyautogui.write(to_type, interval=0.05)`
- **Spoken Feedback**: "Typing"

---

## ⏎ `enter`
- **Action**: Presses the Enter key.
- **Use Case**: Submit a form or send a message.
- **Spoken Feedback**: "🚀 Pressing Enter"

---

## 📺 `open youtube`
- **Action**: Opens YouTube in your default web browser.
- **Implementation**: `webbrowser.open("https://www.youtube.com/")`

---

## 🎯 `reset`
- **Action**: Moves the mouse cursor to the center of the screen.
- **Implementation**: `pyautogui.moveTo(screen_w // 2, screen_h // 2)`

---

## ❌ `close`
- **Action**: Closes the current browser tab or window using `Ctrl + W`.
- **Spoken Feedback**: "Closing window"

---

## 🔼 `scroll up`
- **Action**: Scrolls the page up.
- **Implementation**: `pyautogui.scroll(500)`
- **Spoken Feedback**: "Scrolling up"

---

## 🔽 `scroll down`
- **Action**: Scrolls the page down.
- **Implementation**: `pyautogui.scroll(-500)`
- **Spoken Feedback**: "Scrolling down"
