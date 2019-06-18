#! /usr/bin/env python
#
# Controlled media recording library for the Rasperry-Pi
# Copyright (c) 2015 - 2019 Jolle Jolles <j.w.jolles@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import cv2
import time
import numpy as np

import animlab.utils as alu
import animlab.imutils as alimu

from .videoin import VideoIn

class Calibrate:

    def __init__(self, system="auto", framerate=8, resolution=(640,480),
                 cross = False):

        """
        Opens a video stream with user interface for calibrating the camera
        """

        self.system = system
        self.framerate = framerate
        self.resolution = resolution
        self.cross = cross
        self.stream = True
        self.exit = False

        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        self.m = alimu.mouse_events()
        cv2.setMouseCallback('Image', self.m.draw)

        self.drawer()


    def draw_stream(self):
        alu.lineprint("Streaming video..")

        self.vid = VideoIn(system=self.system, framerate=self.framerate,
                           resolution=self.resolution)
        self.vid.start()

        while True:
            self.img = self.vid.read()

            if self.cross:
                alimu.draw_cross(self.img, self.vid.resolution)

            cv2.imshow("Image", self.img)
            cv2.resizeWindow("Image", self.vid.resolution[0], self.vid.resolution[1])

            k = cv2.waitKey(1) & 0xFF
            if k == ord("c"):
                self.cross = not self.cross
            if k == ord("f"):
                winval = abs(1 - cv2.getWindowProperty('Image', 0))
                cv2.setWindowProperty("Image", 0, winval)
            if k == ord("d"):
                self.stream = False
                break
            if k == 27:
                alu.lineprint("User exited..")
                self.exit = True
                break

        self.vid.stop()


    def draw_frame(self):
        alu.lineprint("Selecting roi..")
        self.imgbak = self.img.copy()

        while True:
            img = self.imgbak.copy()
            alimu.draw_crosshair(img, self.m.pointer)
            alimu.draw_rectangle(img, self.m.pointer, self.m.rect, self.m.drawing)
            cv2.imshow("Image", img)

            k = cv2.waitKey(1) & 0xFF
            if k == ord("s"):
                if self.m.rect and len(self.m.rect) == 2:
                    self.roi = alimu.get_reccoords(self.m.rect)
                    alu.lineprint("roi "+str(self.roi)+" stored..")
                    break
                else:
                    alu.lineprint("Nothing to store..")

            if k == ord("z"):
                if self.m.rect and len(self.m.rect) == 2:
                    alu.lineprint("Creating zoomed image..")
                    rect = alimu.get_reccoords(self.m.rect)
                    zoom = alimu.roi_to_zoom(rect, self.vid.resolution)
                    vid = VideoIn(system=self.system, resolution=(2592,1944),
                                  zoom=zoom)
                    zoomedimg = vid.img()
                    cv2.namedWindow("Zoomed", cv2.WINDOW_NORMAL)
                    while True:
                        cv2.imshow("Zoomed", zoomedimg)
                        xwin = int(zoom[2]*vid.resolution[0])
                        ywin = int(zoom[3]*vid.resolution[1])
                        cv2.resizeWindow("Zoomed", xwin, ywin)

                        k = cv2.waitKey(1) & 0xFF
                        if k == ord("f"):
                            winval = abs(1 - cv2.getWindowProperty('Zoomed', 0))
                            cv2.setWindowProperty("Zoomed", 0, winval)
                        if k == 27:
                            vid.stop()
                            break

                    k = 255
                    cv2.destroyWindow("Zoomed")

            if k == 27:
                self.stream = True
                self.m.rect = ()
                break


    def drawer(self):
        while True:
            if self.stream:
                self.draw_stream()
            if not self.stream:
                self.draw_frame()
            if self.exit:
                cv2.waitKey(1)
                cv2.destroyWindow("Image")
                cv2.destroyWindow("Zoomed")
                cv2.destroyAllWindows()
                for i in range(5):
                    cv2.waitKey(1)
                break

if __name__ == "__main__":
    Calibrate()
