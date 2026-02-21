import cv2
import mediapipe as mp
import time
import os

WIDTH, HEIGHT = 320, 240
COOLDOWN = 0.7
STABILITY_FRAMES = 4

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

def execute_cmd(cmd):
    os.system(cmd)

def count_fingers(lm):
    fingers = 0

    is_right_hand = lm[5].x < lm[17].x

    if is_right_hand:
        thumb_open = lm[4].x < lm[3].x
    else:
        thumb_open = lm[4].x > lm[3].x

    if thumb_open:
        fingers += 1

    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    dips = [7, 11, 15, 19]
    wrist = lm[0]

    for tip, pip, dip in zip(tips, pips, dips):
        cond1 = lm[tip].y < lm[pip].y
        cond2 = lm[tip].y < lm[dip].y
        cond3 = abs(lm[tip].y - wrist.y) > 0.12
        cond4 = abs(lm[tip].y - lm[pip].y) > 0.03

        if cond1 and cond2 and cond3 and cond4:
            fingers += 1

    return fingers

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

last_action_time = 0
last_command = "NONE"
stable_buffer = []

print("Touchless HCI Started... Press 'q' to quit")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    start = time.time()
    results = hands.process(rgb)

    fingers = 0

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        fingers = count_fingers(hand.landmark)

        stable_buffer.append(fingers)
        if len(stable_buffer) > STABILITY_FRAMES:
            stable_buffer.pop(0)

        if len(stable_buffer) == STABILITY_FRAMES and \
           stable_buffer.count(fingers) == STABILITY_FRAMES:

            now = time.time()

            if now - last_action_time > COOLDOWN:

                if fingers == 5:
                    execute_cmd("xdotool key space")
                    last_command = "PLAY / PAUSE"

                elif fingers == 0:
                    execute_cmd("xdotool key m")
                    last_command = "MUTE"

                elif fingers == 1:
                    execute_cmd("xdotool key ctrl+Up")
                    last_command = "VOLUME UP"

                elif fingers == 2:
                    execute_cmd("xdotool key ctrl+Down")
                    last_command = "VOLUME DOWN"

                elif fingers == 3:
                    execute_cmd("xdotool key n")
                    last_command = "NEXT TRACK"

                last_action_time = now

    fps = int(1 / max(0.001, time.time() - start))

    cv2.putText(frame, f"FINGERS: {fingers}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.putText(frame, f"COMMAND: {last_command}",
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

    cv2.putText(frame, f"FPS: {fps}",
                (WIDTH-100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

    cv2.imshow("Touchless Media Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()