import cv2
import pyautogui
import numpy as np
import time
from core.brain import Brain
import easyocr
import keyboard

class GameMaster:
    def __init__(self, app):
        self.app = app
        self.location = app.location
        self.ss_offset = (0, 33)
        self.reader = easyocr.Reader(['en'])
        
    def screenshot(self, name = None):
        return cv2.cvtColor(np.array(pyautogui.screenshot(
            name,
            (
                self.ss_offset[0] + self.location[0],
                self.ss_offset[1] + self.location[1],
                self.app.size[1],
                self.app.size[0]
            )
        )), cv2.COLOR_RGB2BGR)
        
    def recognize_letters(self):
        screenshot = self.screenshot()
        # ss = screenshot.copy()
        # ss = ss[516:862, 103:441]
        mask = cv2.inRange(screenshot, np.array([45, 26, 15]), np.array([65, 46, 35]))
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # draw rectangle over all contours
        delta = 10
        letters = []
        locations = []
        rects = []
        totalx = 0
        totaly = 0
        count = 0
        ss = screenshot.copy()
        for contour in contours:
            # only if the contour is big
            if cv2.contourArea(contour) < 200 or cv2.contourArea(contour) >= 2000:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            if x < 103 or y < 516 or x+w > 441 or y+h > 862:
                continue
            # continue if the contour bounding rect is already inside another bounding rect
            flag = False
            for rect in rects:
                if x > rect[0] and y > rect[1] and x+w < rect[0]+rect[2] and y+h < rect[1]+rect[3]:
                    flag = True
            if flag:
                continue
            cv2.rectangle(ss, (x-delta, y-delta), (x+w+delta, y+h+delta), (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(contour)
            totalx += x+(w//2)
            totaly += y+(h//2)
            count += 1
            rects.append((x, y, w, h))
            gray = cv2.cvtColor(screenshot[y-delta:y+h+delta, x-delta:x+w+delta], cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, (0,0), fx=5, fy=5)
            s:str = self.reader.readtext(gray, detail=0, allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            print(s, cv2.contourArea(contour))
            cv2.drawMarker(ss, (x+(w//2), y+(h//2)), (0, 0, 255), cv2.MARKER_CROSS, 20, 2)
            if len(s) == 0:
                s = "I"
            letters.append(s[0].lower().strip('\n'))
            locations.append((x+self.ss_offset[0]+self.location[0]+(w//2),y+delta+delta+self.ss_offset[0]+self.location[1]+(h//2)))
        path = (totalx//count+self.ss_offset[0]+self.location[0], totaly//count+self.ss_offset[1]+self.location[1])
        
        cv2.imwrite("letters.png", ss)
        print(letters)
        print(locations)
        brain = Brain()
        words = brain.predict(letters)
        print(words)
        for x in words:
            already = {}
            for y in x:
                if keyboard.is_pressed("q"):
                    raise KeyboardInterrupt
                if y in already:
                    i = letters.index(y, max(already[y])+1)
                    already[y].append(i)
                else:
                    i = letters.index(y)
                    already[y] = [letters.index(y)]
                pyautogui.moveTo(*locations[i])
                time.sleep(0.2)
                pyautogui.mouseDown()
                pyautogui.moveTo(*path)
            pyautogui.mouseUp()