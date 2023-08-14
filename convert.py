import pandas as pd
import numpy as np
from tracker import *

# global lst
# lst = []

class convert:
    def __init__(self):
        pass

    def to_dataframe(self,boxes,count,class_ids):
        px = pd.DataFrame(boxes).astype(float)
        px['frame'] = count
        px['class'] = class_ids
        return px
    
    def to_list(self,df):
        lst = []
        for idx,row in df.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            cls = int(row['class'])

            # if cls in [2,5,7,67]:
            #     lst.append([x1,y1,x2,y2,cls])
            lst.append([x1,y1,x2,y2,cls])
        return lst