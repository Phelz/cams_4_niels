import numpy as np
import cv2
import time
from datetime import datetime
import os


# No 47 48 49
# CAM_LIST = np.hstack( (np.arange(35, 47), np.arange(50, 70) ))
CAM_LIST = np.array( [40, 41, 42] )

camera_resources = {}
for cam_num in CAM_LIST:
    print(f'Opening Stream for Cam # {cam_num:2d}')

    # open a video stream
    cap = cv2.VideoCapture(f"rtsp://alphacam:maxalpha@alphacam{cam_num:2d}.cern.ch/stream1") 
    
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    camera_resources[cam_num] = {
        'capture': cap,
        'width': w,
        'height': h,
        'fps': fps,
        'fourcc': fourcc
    }
    
    print(f'Successfully Opened Stream for Cam # {cam_num:2d}')


while True:
    dt  = datetime.now().isoformat().replace(':','-').replace('.','-')

    for cam_num in CAM_LIST:
        # print(f'Obtaining Feed for Cam # {cam_num}')
        # print(f'{camera_resources[cam_num]['fourcc']}')
        out = cv2.VideoWriter(f'log\\cam_{cam_num:2d}_output_{dt}.mp4',  
                              camera_resources[cam_num]['fourcc'], 
                              camera_resources[cam_num]['fps'],
                              (int(camera_resources[cam_num]['width']), int(camera_resources[cam_num]['height']))
                            )
        
        camera_resources[cam_num]['out'] = out


    # start timer
    start_time = time.time()

    # Capture video from camera per 60 seconds
    while (int(time.time() - start_time) < 60):

        c1 = CAM_LIST[0]
        c2 = CAM_LIST[1]
        c3 = CAM_LIST[2]

        ret1, frame1 = camera_resources[c1]['capture'].read()
        ret2, frame2 = camera_resources[c2]['capture'].read()
        ret3, frame3 = camera_resources[c3]['capture'].read()

        out1 = camera_resources[c1]['out']
        out2 = camera_resources[c2]['out']
        out3 = camera_resources[c3]['out']

        if ret1 and ret2 and ret3:


            #frame = cv2.flip(frame,0) # Do you want to FLIP the images?

            out1.write(frame1)
            out2.write(frame2)
            out3.write(frame3)


            img = np.concatenate((frame1, frame2, frame3), axis=1)
            # img = 

            cv2.imshow('frame',img)
            # cv2.imshow('frame',frame2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    # Release everything if job is finished
    for cam_num in CAM_LIST:
        print('Releasing')
        camera_resources[cam_num]['out'].release()

        list_of_files = os.listdir('log')
        cam_num_path = f"log\\cam_{cam_num}"
        full_path = [cam_num_path + "{0}".format(x) for x in list_of_files]

        if len(list_of_files) == 15*len(CAM_LIST): # Delete keep at most 15 files from each cam, this can be refined to do this properly
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)

cap.release()

cv2.destroyAllWindows()