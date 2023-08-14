import numpy as np
import cv2
from utils import *

ut = utils()

class speed:
    def __init__(self):
        self.id_ = {}

    def plot_region(self,config,frame):
        s_region1 = config[0]['speed_region']['region_1']
        s_region2 = config[0]['speed_region']['region_2']
        image = cv2.polylines(frame,[np.array(s_region1, np.int32)], True, (0,255,255), 3)
        image = cv2.polylines(frame,[np.array(s_region2, np.int32)], True, (80,255,15), 3)
        # image = cv2.polylines(frame,[np.array(region4, np.int32)], True, (0,0,255), 3)
        return image

    def check_speed(self,boxes,config,frame,fps):
        result = 0
        
        s_region1 = config[0]['speed_region']['region_1']
        s_region2 = config[0]['speed_region']['region_2']
        # print('bbbb',boxes)
        # for i in range(len(boxes)):
        # for box in boxes:
            # print(box)
        xa,ya,xb,yb = ut.yolobbox2bbox(boxes=boxes)
        # print(xa,ya,xb,yb)
        _,_,_,_,cls_id,id = boxes
        if cls_id in [0, 9, 10, 11, 16, 17, 18]:
            isregion1LB = cv2.pointPolygonTest(np.array(s_region1, np.int32),((xa,yb)),False)
            isregion1RB = cv2.pointPolygonTest(np.array(s_region1, np.int32),((xb,yb)),False)
            isregion2LB = cv2.pointPolygonTest(np.array(s_region2, np.int32),((xa,yb)),False)
            isregion2RB = cv2.pointPolygonTest(np.array(s_region2, np.int32),((xb,yb)),False)
                
            if isregion1LB < 0 and isregion1RB < 0 and isregion2LB < 0 and isregion2RB < 0:
                self.id_[id] = 1
                # print(self.id_)

            if isregion1LB >= 0 and isregion1RB >= 0:
                if id in self.id_:
                    self.id_[id] += 1
                    # print(self.id_)
                # if id not in self.id_:
                else:
                    self.id_[id] = 0
                    # print(self.id_)

            if isregion2LB >= 0 and isregion2RB >= 0:
                if id not in self.id_:
                    self.id_[id] = np.inf
                else:
                    val = self.id_.get(id)
                    # print(val)
                    if val == 0:
                        pass
                    speed = round(15 * (fps / (val)) * (18/5),2)
                        # print("id: ",id," speed: ",speed)
                    if speed == 0:
                        # cv2.putText(frame, str('Not Detectable'), (xa+20,ya+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
                        pass
                    elif speed > 30 and speed < 100:
                        cv2.putText(frame, str(speed), (xa+20,ya+10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
                        result = 1

        return cls_id,result