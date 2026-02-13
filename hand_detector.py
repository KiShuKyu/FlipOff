import cv2 as cv
import mediapipe as mp
import math


class HandDetector:
    def __init__(self, detection_conf=0.7, tracking_conf=0.7):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if draw and self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img, handLms, self.mpHands.HAND_CONNECTIONS
                )

        return img

    def find_landmarks(self, img):
        lm_list = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            h, w, _ = img.shape

            for i, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((i, cx, cy))

        return lm_list

    @staticmethod
    def distance(p1, p2):
        return math.hypot(p2[1] - p1[1], p2[2] - p1[2])
