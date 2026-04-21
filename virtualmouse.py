import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import threading
import tkinter as tk
from tkinter import messagebox

running = False

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Screen and smoothing
screen_w, screen_h = pyautogui.size()
smooth_factor = 5
prev_loc_x, prev_loc_y = 0, 0
drag_mode = False

# --- Helper Function ---
def dist(x1, y1, x2, y2):
    """Calculates the hypotenuse between two points."""
    return np.hypot(x2 - x1, y2 - y1)

# --- Mouse Control Function 
def start_virtual_mouse():
    global running, prev_loc_x, prev_loc_y, drag_mode
    running = True
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        messagebox.showerror("Error", "Could not open webcam.")
        return

    while running:
        success, img = cam.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        img_h, img_w, _ = img.shape

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                lm_list = hand_landmarks.landmark

                #fingertip coordinates
                index_x, index_y = int(lm_list[8].x * img_w), int(lm_list[8].y * img_h)
                thumb_x, thumb_y = int(lm_list[4].x * img_w), int(lm_list[4].y * img_h)
                middle_x, middle_y = int(lm_list[12].x * img_w), int(lm_list[12].y * img_h)
                ring_x, ring_y = int(lm_list[16].x * img_w), int(lm_list[16].y * img_h)

                # screen coordinates
                screen_x = np.interp(index_x, (100, img_w - 100), (0, screen_w))
                screen_y = np.interp(index_y, (100, img_h - 100), (0, screen_h))

                # Smooth cursor movement
                curr_x = prev_loc_x + (screen_x - prev_loc_x) / smooth_factor
                curr_y = prev_loc_y + (screen_y - prev_loc_y) / smooth_factor
                pyautogui.moveTo(curr_x, curr_y)
                prev_loc_x, prev_loc_y = curr_x, curr_y

                # Gesture distances
                d_thumb_index = dist(index_x, index_y, thumb_x, thumb_y)
                d_index_middle = dist(index_x, index_y, middle_x, middle_y)
                d_index_ring = dist(index_x, index_y, ring_x, ring_y)

                # --- GESTURE RECOGNITION ---
                # Left Click / Drag
                if d_thumb_index < 25: # Pinch gesture
                    if not drag_mode:
                        pyautogui.mouseDown()
                        drag_mode = True

                # --- SCROLL (index + middle) ---
                elif d_index_middle < 35:
                    pyautogui.scroll(-80)
                    cv2.putText(img, "Scroll", (30, 110),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                # --- RIGHT CLICK (index + ring) ---
                elif d_index_ring < 35:
                    pyautogui.click(button='right')
                    cv2.putText(img, "Right Click", (30, 160),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

                # Release Drag / Perform Click
                elif d_thumb_index >= 30:
                    if drag_mode:
                        pyautogui.mouseUp()
                        drag_mode = False
                        pyautogui.click() # Register as a click on release

        cv2.imshow("AI Virtual Mouse", img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    running = False

# --- Stop Function ---
def stop_virtual_mouse():
    global running
    running = False
    root.after(100, root.quit) # Quit the GUI after stopping the thread


# --- Thread Wrapper (prevents GUI freeze) ---
def start_thread():
    threading.Thread(target=start_virtual_mouse, daemon=True).start()

# --- GUI Setup ---
root = tk.Tk()
root.title("🖱 AI Virtual Mouse")
root.geometry("900x700")
root.config(bg="#101820")

messagebox.showinfo("AI Virtual Mouse", "Press 'Start' to begin and 'q' in the video window to stop.")


title = tk.Label(root, text="AI Virtual Mouse", font=("Helvetica", 40, "bold"),
                 fg="#00FFAA", bg="#101820")
title.pack(pady=40)

desc = tk.Label(root, text="Control your cursor using hand gestures\nvia webcam!",
                font=("Helvetica", 12), fg="white", bg="#101820")
desc.pack(pady=15)

start_btn = tk.Button(root, text="▶ Start Virtual Mouse", font=("Helvetica", 40, "bold"),
                      bg="#00FFAA", fg="#101820", width=44, command=start_thread)
start_btn.pack(pady=15)

stop_btn = tk.Button(root, text="⏹ Stop", font=("Helvetica", 40, "bold"),
                     bg="#FF3B3B", fg="white", width=44, command=stop_virtual_mouse)
stop_btn.pack(pady=15)

footer = tk.Label(root, text="Developed by Shrey using Python, OpenCV & MediaPipe",
                  font=("Helvetica", 9), fg="#AAAAAA", bg="#101820")
footer.pack(side="bottom", pady=15)

root.mainloop()
