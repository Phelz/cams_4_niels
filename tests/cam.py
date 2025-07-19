import numpy as np
import cv2
import time
from datetime import datetime
import os


# No 47 48 49
CAM_LIST = np.hstack( (np.arange(35, 47), np.arange(50, 70) ))
print(CAM_LIST)


# camera_resources = {}
# for cam_num in CAM_LIST:


# open a video stream
cap = cv2.VideoCapture("rtsp://alphacam:maxalpha@alphacam42.cern.ch/stream1") # Do you want to test with the local camera?

w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS) 
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# open a video stream
cap2 = cv2.VideoCapture("rtsp://alphacam:maxalpha@alphacam40.cern.ch/stream1") # Do you want to test with the local camera?

w2= cap2.get(cv2.CAP_PROP_FRAME_WIDTH)
h2 = cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps2 = cap2.get(cv2.CAP_PROP_FPS) 
fourcc2 = cv2.VideoWriter_fourcc(*'mp4v')


while True:
    dt  = datetime.now().isoformat().replace(':','-').replace('.','-')
    out = cv2.VideoWriter('log\\output' + dt + '.mp4', fourcc, fps, (int(w),int(h)))
    out2 = cv2.VideoWriter('log\\output' + dt + '.mp4', fourcc2, fps2, (int(w2),int(h2)))

    # start timer
    start_time = time.time()

    # Capture video from camera per 60 seconds
    while (int(time.time() - start_time) < 60):
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()
        if ret==True:

            #frame = cv2.flip(frame,0) # Do you want to FLIP the images?

            out.write(frame)
            out2.write(frame2)

            img = np.concatenate((frame, frame2), axis=0)

            cv2.imshow('frame',img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    out.release()

    list_of_files = os.listdir('log')
    full_path = ["log\\{0}".format(x) for x in list_of_files]

    if len(list_of_files) == 15:
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)

cap.release()

cv2.destroyAllWindows()