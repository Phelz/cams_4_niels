# SERVER_IP = '128.141.240.230' # ! ATRAP Room, ALPHACPC47
SERVER_IP = '0.0.0.0' # ! ATRAP Room, ALPHACPC47
QUART_SERVER_PORT = 5000
DASH_APP_PORT = 8050

DELAY_BETWEEN_FRAMES = 2 # ! add delay (in seconds) if CPU usage is too high

# ! How Niels wants to cluster cameras.
CAMS_LABELS = {
    'Zone': [37, 38, 39, 41, 45, 52, 54, 56, 57, 59, 60, 61, 67],
    'Platform': [35, 40, 43, 51, 57, 60, 62, 63, 65, 66, 68],
    'Equipment' : [42, 44, 53, 69],
    'Helium': [39, 40, 61, 67 ],
    'Rooms' : [34, 36, 47, 48, 64, 69,]
}

ALL_CAMS_IDS = [cam_id for cam_ids in CAMS_LABELS.values() for cam_id in cam_ids]



def get_camera_rtsp_path(cam_id:int) -> str:
    ''' Get the RTSP path for a given camera ID.'''
    
    # ! Unfortunately, needs to be hardcoded, since not all use maxalpha.
    if 34 <= int(cam_id) <= 43:
        return f"rtsp://alphacam:maxalpha@alphacam{cam_id}.cern.ch/stream1"
    elif 44 <= int(cam_id) <= 48:
        return f"rtsp://alphacam:Maxalpha@alphacam{cam_id}.cern.ch/stream1"
    elif int(cam_id) >= 50:
        return f"rtsp://alpha-admin:Nmt30smiAg$@alphacam{cam_id}.cern.ch/stream1"
    else:
        return None
    