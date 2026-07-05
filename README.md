# RC-Drone-School-Project

[assets/drone.jpeg](assets/drone.jpeg)

A repo containing all the code for a RC Drone University course using Micropython as the language.

# About
A repository that has the files used for a school project, a remote controlled 2 wheeled drone. The drone has simple electronics, A Raspberry Pico W, Dual H-Bridge for controlling motors and the actual motors. It is powered by 7 AA-batteries.

**laptop.py** The program to run on a computer to act as the remote controller.
**main.py** The program the Raspberry Pi runs.


# Instructions
1. Open terminal and clone the repo:
2. git clone https://github.com/jerejaakonaho/RC-Drone-School-Project
3. cd RC-DRONE-School-Project
4. Create virtual environment: venv\Scripts\activate (windows)
5. Install dependencies: pip install -r requirements.txt
6. Install tkinter (sudo apt install python3-tk) on linux
7. Import the main.py to a Raspberry Pico W (Update the WiFi settings)
8. Run the laptop.py (replace ip with the one provided in Thonny after main.py is ran)
9. GUI window opens up that registers key presses and sends them to the Pico using UDP.
