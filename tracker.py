import numpy as np
import cv2
import math
global centre_points_previous
centre_points_previous = []

class tracker:
    # def __init__(self,type):
    #     self.type = type
        
    #     if self.type == 'BOOSTING':
    #         self.tracker = cv2.TrackerBoosting_create()
    #     if self.type == 'MIL':id
    #         self.tracker = cv2.TrackerMIL_create()
    #     if self.type == 'KCF':
    #         self.tracker = cv2.TrackerKCF_create()
    #     if self.type == 'TLD':
    #        self.tracker = cv2.TrackerTLD_create()
    #     # if self.type == 'MEDIANFLOW':
    #     #     self.tracker = cv2.TrackerMedianFlow_create()
    #     if self.type == 'GOTURN':
    #         self.tracker = cv2.TrackerGOTURN_create()
    #     if self.type == 'MOSSE':
    #         self.tracker = cv2.TrackerMOSSE_create()
    #     if self.type == "CSRT":
    #         self.tracker = cv2.TrackerCSRT_create()

    # def get_center(self,img,box):
    #     (x,y,w,h) = box
    #     cx = int((x+x+w)/2)
    #     cy = int((y+y+h)/2)
    #     box.append(cx)
    #     box.append(cy)
    #     cv2.circle(img, (cx, cy), 5, (0, 0, 255), -1)
    #     return box

    # def start_tracker(self,frame,bbox):
    #     # Initialize tracker with first frame and bounding box
    #     ok = self.tracker.init(frame, bbox)
    #     # Update tracker
    #     ok, bbox = tracker.update(frame)
    #     return bbox

    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0


    def update(self, objects_rect):
        # Objects boxes and ids
        new_center_points = []
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h, cls = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            # new_center_points.append((cx,cy))

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                # print(f"dist of veh{id} is {dist}")

                if dist < 120:
                    #count = 3
                    self.center_points[id] = (cx, cy)
                    # print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, cls, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, cls, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _,_, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        # center_points_previous = new_center_points.copy()
        return objects_bbs_ids,self.center_points
        # return new_center_points,center_points_previous