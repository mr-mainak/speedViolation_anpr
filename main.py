import cv2
import pandas as pd
from detection import *
from tracker import *
from convert import *
from speed import *
from utils import *
from application import *
import yaml
import json
import argparse

parser = argparse.ArgumentParser(description='parameters to run')
parser.add_argument('--p', default=False, help='path_to_video')
parser.add_argument('--ow',default=False, help='path to your object detection weights file')
parser.add_argument('--oc',default=False, help='path to your object detection config file')
parser.add_argument('--lw',default=False, help='path to your lpd weight file')
parser.add_argument('--lc',default=False, help='path to your lpd config file')
parser.add_argument('--o', default=False, help='output to save evidence')
args = parser.parse_args()

# Use this for vedio
cap = cv2.VideoCapture(args.p)
net = detection(args.ow,args.oc)
conv = convert()
track = tracker()
anpr = lpd_detection(args.lw,args.lc)
spd = speed()
ut = utils()

classes = []
with open('dnn_model/labels.txt','r') as c:
    for class_name in c.readlines():
        class_name = class_name.strip()
        classes.append(class_name)

count = 0  
count_img = 0      

with open("laneConfig.yaml", "r") as yamlfile:
    config_data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Read Successful")

id_store = {}

while True:
# for i in folder:
    #If using a video
    ret, frame = cap.read()
    # print(frame.shape)
    count += 1
    print("*****************",count,"*******************")
    class_ids,_,bboxes = net.detect(file=frame)
    
    #Convert to bbox to list
    px = conv.to_dataframe(bboxes,count,class_ids)
    print(px)
    l = conv.to_list(px)
    # print('list: ', l)

    #Tracker
    id,centre = track.update(objects_rect=l)
    print("id: ",id)

    #Plot the regions
    frame = spd.plot_region(config=config_data,frame=frame)
    left = config_data[0]["trigger_line"]["line"][0]
    right = config_data[0]["trigger_line"]["line"][1]
    cv2.line(frame, left, right, color = (0, 255, 0))
    for i in id:
        # Speed Detection
        c,r = spd.check_speed(boxes=i,config=config_data,frame=frame,fps=13)
        # print("III",c)

        #Trigger Line
        cropped_img = ut.isbelow(config=config_data,boxes=id,image=frame)
        if cropped_img is not None:
            if r != 0:
                _,_,_,_,_,obj_id = i
                if obj_id not in id_store:
                    id_store[obj_id] = 1
                    cv2.imwrite(f'./{args.o}/image_{count_img}_img.png', cropped_img)
                    class_ids,_,bboxes = anpr.detect(file=cropped_img)
                    # print(bboxes)
                    if len(bboxes) != 0:
                        bboxes[0].append(0)
                        bboxes[0].append(0)
                        xa,ya,xb,yb = ut.yolobbox2bbox(bboxes[0])
                        plates = cropped_img[ya:yb,xa:xb]
                        cv2.imwrite(f'./{args.o}/image_{count_img}_lp.png', plates)
                        text = ut.get_number(image=plates)
                        if len(text) != 0:
                            data = {"obj_id":obj_id, "class":ut.convert2labels(c),"plate_no":text[0],"image_id":count_img}
                            with open("output.json", "a") as outfile:
                                json.dump(data, outfile, indent=4)
                        
                        count_img += 1
                else:
                    pass
    
    # Resize
    # cv2.resize(frame, (200,200)) 
    cv2.imshow('Frame',frame)
    # cv2.imshow('Mask',mask)

    key = cv2.waitKey(0)
    # key = cv2.waitKey(30) #For each whole video
        
    # output.write(frame)
    # op.write(frame)
        
    if key == 27:
        break

# print(len(boxes))

cap.release()
# output.release()
# op.release()
cv2.destroyAllWindows()
