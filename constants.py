import cv2
import os
import socket
import time

#time.sleep(15)
#my_ip = socket.gethostbyname(socket.gethostname())
#my_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
my_ip='192.168.0.42'
print(my_ip)

if os.name == 'nt':
    FORMAT_DIR = '\\' # Windows
    IS_WINDOWS = True
else:
    FORMAT_DIR = '/' # Linux
    IS_WINDOWS = False

WINDOW_NAME = 'Photo Booth'
COUNT_DOWN = 5

i= cv2.imread('/home/pi/Photobooth/AbbyFrame3.png',-1)
i2= cv2.imread('/home/pi/Photobooth/AbbyFrame.png',-1)

#background= cv2.resize(i,(int(i.shape[1]/1.5),int(i.shape[0]/1.7)))

background= cv2.resize(i,(640,430))
background2= cv2.resize(i2,(640,430))

bgf= cv2.resize(i,(2144,1424))
bgf2= cv2.resize(i2,(2144,1424))

i= cv2.imread('/home/pi/Photobooth/bg3.png',-1)
bg2= cv2.resize(i,(int(i.shape[1]/1.5),int(i.shape[0]/1.7)))

img_button= cv2.imread('/home/pi/Photobooth/start_button.png',-1)

attendez= cv2.imread('/home/pi/Photobooth/attendez.png',-1)

bg_height, bg_width, _ = background.shape
img_height, img_width, _ = img_button.shape

offset =(280,300)

button_pos = [offset[0], offset[1],offset[0]+img_width,offset[1]+img_height]
buttonf_pos = [700, 300,1000,600]