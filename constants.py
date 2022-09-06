import cv2
import os
import socket
import time

#time.sleep(15)
#my_ip = socket.gethostbyname(socket.gethostname())
#my_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
my_ip='10.3.141.1'
address='/home/pi/Photobooth/'
print(my_ip)

if os.name == 'nt':
    FORMAT_DIR = '\\' # Windows
    IS_WINDOWS = True
else:
    FORMAT_DIR = '/' # Linux
    IS_WINDOWS = False

WINDOW_NAME = 'Photo Booth'
COUNT_DOWN = 5



#background= cv2.resize(i,(int(i.shape[1]/1.5),int(i.shape[0]/1.7)))


#bgf= cv2.resize(i,(2144,1424))


i= cv2.imread(address + 'frame/boda1.png',-1)
background= cv2.resize(i,(640,430))
background_HR= cv2.resize(i,(2144,1424))

i= cv2.imread(address + 'views/scan_page.png',-1)
scan_page= cv2.resize(i,(int(i.shape[1]/1.5),int(i.shape[0]/1.7)))
flash_page= cv2.imread(address + 'views/flash_page.png',-1)

img_button= cv2.imread(address + 'images/start_button.png',-1)


bg_height, bg_width, _ = background.shape
img_height, img_width, _ = img_button.shape

offset =(280,300)

button_pos = [offset[0], offset[1],offset[0]+img_width,offset[1]+img_height]
buttonf_pos = [700, 300,1000,600]