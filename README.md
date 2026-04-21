# virtual-mouse
The AI Virtual Mouse is an advanced computer vision-based system that allows users to control a computer cursor using hand gestures, eliminating the need for a physical mouse. This project focuses on creating a touchless and intuitive human-computer interaction system, addressing the growing demand for contactless technology in modern environments.
The primary objective of this project is to design and implement a virtual mouse capable of performing essential mouse operations such as cursor movement, left click, right click, scrolling, and drag-and-drop through real-time hand gesture recognition. The system captures live video input using a webcam and processes it to detect and track hand movements efficiently.

The implementation is carried out using Python, leveraging powerful libraries such as OpenCV for video processing, MediaPipe for accurate hand landmark detection, PyAutoGUI for controlling system-level mouse actions, and Tkinter for developing a user-friendly graphical interface.

The final system demonstrates high accuracy and real-time responsiveness, showcasing the practical application of computer vision in building innovative, touchless interfaces. This project highlights the potential of gesture-based systems in enhancing accessibility, usability, and future human-computer interaction technologies.

Workflow Explanation

The system captures video from the webcam and processes each frame using OpenCV. MediaPipe detects hand landmarks and tracks finger positions. Based on predefined gesture rules (e.g., index + thumb = click), actions are triggered. PyAutoGUI converts these gestures into system-level mouse operations. Tkinter provides a GUI to control the application.

Block Diagram
Webcam → OpenCV → MediaPipe → Hand Landmarks → Gesture Detection → PyAutoGUI → Mouse Actions → Tkin
