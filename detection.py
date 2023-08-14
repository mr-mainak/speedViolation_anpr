import numpy as np
import cv2

class detection:
    def __init__(self,path_weights,path_cfg):
        self.path_weights = path_weights
        self.path_cfg = path_cfg

    def detect(self,file):
        net = cv2.dnn.readNet(self.path_weights,self.path_cfg)
        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(256,256),scale=1/255)
        class_ids,scores,bboxes = model.detect(file, confThreshold=0.3, nmsThreshold=.4)
        
        ids,boxes,sco= [],[],[]

        for i in range(len(class_ids)):
            ids.append(class_ids[i])
            boxes.append(scores[i])
            sco.append(list(bboxes[i]))
        return ids,boxes,sco
    
class lpd_detection:
    def __init__(self,path_weights,path_cfg):
        self.path_weights = path_weights
        self.path_cfg = path_cfg

    def detect(self,file):
        net = cv2.dnn.readNet(self.path_weights,self.path_cfg)
        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(256,256),scale=1/255)
        class_ids,scores,bboxes = model.detect(file, confThreshold=0.3, nmsThreshold=.4)
        ids,boxes,sco= [],[],[]
        for i in range(len(class_ids)):
            ids.append(class_ids[i])
            boxes.append(scores[i])
            sco.append(list(bboxes[i]))
        return ids,boxes,sco
    