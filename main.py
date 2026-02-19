import cv2 as cv
import time
# import os   # UNCOMMENT ONLY WHEN YOU TRUST IT

from hand_detector import HandDetector
from gesture_logic import GestureRecognizer


def main():
    cap = cv.VideoCapture(0)
    detector = HandDetector()
    recognizer = GestureRecognizer(hold_time=1.5)

    p_time = 0
    shutdown_triggered = False

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.find_hands(img)
        landmarks = detector.find_landmarks(img)

        if landmarks:
            if recognizer.detect_shutdown_gesture(landmarks):
                cv.putText(
                    img, "SHUTDOWN GESTURE CONFIRMED",
                    (40, 80), cv.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 0, 255), 2
                )

                if not shutdown_triggered:
                    print("Shutdown gesture detected.")
                    shutdown_triggered = True

                    # FINAL STEP (COMMENTED FOR SAFETY)
                    # os.system("shutdown /s /t 5")

        c_time = time.time()
        fps = int(1 / (c_time - p_time)) if c_time != p_time else 0
        p_time = c_time

        cv.putText(img, f"FPS: {fps}", (20, 40),
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv.imshow("Gesture Control", img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
