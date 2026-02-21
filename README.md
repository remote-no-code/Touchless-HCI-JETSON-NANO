# Touchless HCI System for Media Control (NVIDIA Jetson Nano)

## Project Overview
This project implements a Touchless Human-Computer Interaction (HCI) system deployed on edge hardware. It translates real-time hand gestures into media control commands (Play/Pause, Mute, Volume Up/Down, Next Track) for local applications like VLC. 

Built specifically for the **NVIDIA Jetson Nano**, the system utilizes the MediaPipe Hands framework for edge computer vision and maps recognized gestures to system-level keyboard shortcuts via the Linux `xdotool` utility.

## Key Features
* **Custom Joint-Logic Processing:** Implements a strict mathematical check of Proximal (PIP) and Distal (DIP) joints to prevent half-folded fingers from triggering false actions.
* **Dynamic Thumb Tracking:** Automatically detects whether the user is raising their left or right hand by comparing Index and Pinky MCP joints, ensuring accurate thumb-state calculation.
* **Hardware Stability Filter:** Utilizes a custom multi-frame stability buffer that requires a gesture to be held consistently across consecutive frames before executing a command, preventing rapid CPU-locking command spam.
* **Edge-Optimized:** Capped at 320x240 resolution with `model_complexity=0` to ensure stable framerates (>15 FPS) and low-latency inference on the Jetson Nano's ARM architecture.

## Hardware & Software Requirements
* **Hardware:** NVIDIA Jetson Nano (4GB), USB Webcam
* **OS:** JetPack 4.6 (Ubuntu 18.04)
* **Dependencies:** Python 3.6, OpenCV, MediaPipe, `xdotool`

## Installation Instructions

Because the Jetson Nano runs on `aarch64` architecture, standard pip installations for MediaPipe may fail. Follow these specific steps to deploy the environment:

**1. Install System Dependencies:**
```bash
sudo apt-get update
sudo apt-get install -y xdotool python3-opencv python3-pip

```

**2. Install Python Packages:**
*(Note: If the standard `requirements.txt` fails to build MediaPipe on the Jetson Nano, use the pre-compiled wheel below).*

```bash
pip3 install dataclasses numpy==1.19.4
pip3 install [https://github.com/PINTO0309/mediapipe-bin/releases/download/v0.8.5/mediapipe-0.8.5_cuda102-cp36-cp36m-linux_aarch64.whl](https://github.com/PINTO0309/mediapipe-bin/releases/download/v0.8.5/mediapipe-0.8.5_cuda102-cp36-cp36m-linux_aarch64.whl)
pip3 install -r requirements.txt

```

## Usage

1. Open a media player (e.g., VLC or Spotify) in the background.
2. Run the main execution script:

```bash
python3 arm.py

```

3. A window titled "Touchless Media Control" will appear. Perform gestures in front of the webcam to control your media. Press `q` while focused on the video window to quit.

## Gesture Mapping

| Gesture / Fingers | Action | System Command Executed |
| --- | --- | --- |
| **5 Fingers (Open Palm)** | Play / Pause | `Space` |
| **0 Fingers (Closed Fist)** | Mute | `m` |
| **1 Finger (Index Up)** | Volume Up | `Ctrl + Up` |
| **2 Fingers (Index + Middle)** | Volume Down | `Ctrl + Down` |
| **3 Fingers** | Next Track | `n` |

## Author

**Atharv Aggarwal**
**Tushar Vats**
**Shreya Gupta**
