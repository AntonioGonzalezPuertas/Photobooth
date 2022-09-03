#!/usr/bin/env python
import cv2
import os
import time
import numpy as np
import datetime
import gphoto2 as gp
import io
from PIL import Image
import myScheduler
import schedule
from constants import *
import qrcode
import threading
from flask import Flask, render_template, send_file

#from DigiCam.Camera import Camera
#import winsound

""" ///////// Global ///////// """
start = False
preview_on = True

bg_choose = 1
interval = 0
count_down = COUNT_DOWN
camera = gp.check_result(gp.gp_camera_new())
myScheduler = myScheduler.Scheduler()
"""///////////////////////////////"""


class CameraPB(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.board = 1

    def take_picture(self):
        print ("[INFO] Taking picture")
        #camera = gp.Camera()
        #camera.init()
        config_widget = gp.gp_camera_get_single_config(camera, 'autofocusdrive')
        config_widget = config_widget[1]
        config_set_response = gp.gp_widget_set_value(config_widget, 1)
        print('set response:', gp.gp_widget_get_value(config_widget))
        gp.gp_camera_set_single_config(camera, 'autofocusdrive', config_widget)

        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
        print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        target = os.path.join(os.getcwd(), "/home/pi/Photobooth/capture_0.jpg")
        print('Copying image to', target)
        camera_file = camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(target)
        camera.exit()
        #img = cv2.imread('testing_0.jpg')
        #cv2.imshow('image',img)





    def addImage(self,background,image,pos=(0,0)):
        #get position and crop pasting area if needed
        y = pos[0]
        x = pos[1]
        new_background = background.copy()
        bgWidth = new_background.shape[0]
        bgHeight = new_background.shape[1]
        frWidth = image.shape[0]
        frHeight = image.shape[1]
        width = bgWidth-x
        height = bgHeight-y
        if frWidth<width:
            width = frWidth
        if frHeight<height:
            height = frHeight
        # normalize alpha channels from 0-255 to 0-1
        alpha_background = new_background[x:x+width,y:y+height,3] / 255.0
        alpha_foreground = image[:width,:height,3] / 255.0
        # set adjusted colors
        for color in range(0, 3):
            fr = alpha_foreground * image[:width,:height,color]
            bg = alpha_background * new_background[x:x+width,y:y+height,color] * (1 - alpha_foreground)
            new_background[x:x+width,y:y+height,color] = fr+bg
        # set adjusted alpha and denormalize back to 0-255
        new_background[x:x+width,y:y+height,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255
        i= cv2.resize(new_background,(int(background.shape[1]*1.1),int(background.shape[0]*1.05)))

        return i

    def showText(self,background,text,pos=(0,0)):
        #get position and crop pasting area if needed
        x = pos[0]
        y = pos[1]
        bgWidth = background.shape[0]
        bgHeight = background.shape[1]


        cv2.putText(background,text,org=(x,y), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale= 8,color=(255,255,255))
        cv2.imshow(WINDOW_NAME, background)



    # function that handles the mousclicks
    def process_click(self,event, x, y,flags, params):
        global start, interval,preview_on
        # check if the click is within the dimensions of the button
        if event == cv2.EVENT_LBUTTONDOWN:
            if x > button_pos[0] and y > button_pos[1] and x < button_pos[2] and y < button_pos[3]:
                interval = time.time()
                start=True
                print("Countdown")
            if x > buttonf_pos[0] and y > buttonf_pos[1] and x < buttonf_pos[2] and y < buttonf_pos[3]:
                preview_on = True
                print("Preview")


    def run(self):
        global start, interval,count_down, preview_on

        print("[INFO] Running PhotoBooth")

        cv2.namedWindow(WINDOW_NAME,cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        gp.check_result(gp.gp_camera_init(camera))

        config_widget = gp.gp_camera_get_single_config(camera, 'imagesize')
        config_widget = config_widget[1]
        config_set_response = gp.gp_widget_set_value(config_widget, "2144x1424")
        print('set response:', gp.gp_widget_get_value(config_widget))
        gp.gp_camera_set_single_config(camera, 'imagesize', config_widget)

        #output= addImage(background,img_button,(offset[0],offset[1]))
        #cv2.imshow(WINDOW_NAME, output)

        cv2.setMouseCallback(WINDOW_NAME, self.process_click)


        while True:
            #schedule.run_pending()

            if preview_on:
                camera_file = gp.check_result(gp.gp_camera_capture_preview(camera))
                file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))

                image = Image.open(io.BytesIO(file_data))
                rgb = np.array(image)
                # Convert RGB to BGR
                rgba = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGBA)
                image_flip= cv2.flip(rgba, 1)
                if bg_choose == 0:
                    img_prev= self.addImage(image_flip, background,(0,0))
                else:
                    img_prev= self.addImage(image_flip, background2,(0,0))



            if start:
                counting = time.time() - interval
                if counting >1:
                    print (count_down)
                    #showText(background,str(count_down),(300,280))
                    cv2.putText(img_prev,str(count_down),org=(300,280), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale= 8,color=(255,255,255))
                    interval = time.time()

                    if count_down == 0:
                        #white_background = np.zeros([bg_height ,bg_width,1],dtype=np.uint8)
                        #white_background.fill(255)
                        img_prev = attendez
                        preview_on = False


                    if count_down<0:
                        count_down=COUNT_DOWN
                        start=False

                        self.take_picture()
                        target = os.path.join(os.getcwd(), "/home/pi/PhotoBooth/capture_0.jpg")
                        os.system('cp /home/pi/PhotoBooth/capture_0.jpg /media/pi/AntonioGP/photos/' + str(int(time.time())) + '.jpg')
                        img= cv2.imread(target,-1)
                        b_channel, g_channel, r_channel = cv2.split(img)
                        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  #creating a dummy alpha channel image.
                        img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

                        cv2.imwrite('/home/pi/PhotoBooth/image.jpg',img_BGRA)

                        image_flip= cv2.flip(img_BGRA, 1)
                        print(image_flip.shape[0],image_flip.shape[1])

                        if bg_choose == 0:
                            img_BGRA= self.addImage(image_flip,bgf,(0,0))

                        else:
                            img_BGRA= self.addImage(image_flip,bgf2,(0,0))



                        cv2.imwrite('/home/pi/PhotoBooth/image.jpg',img_BGRA)

                        i= cv2.resize(img_BGRA,(int(background.shape[1]/1.5),int(background.shape[0]/1.5)))
                        posx=330
                        posy=30
                        img_prev= self.addImage(bg2,i,(posx,posy))

                        qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_H,
                            box_size=10,
                            border=4,
                        )
                        qr.add_data('http://' + my_ip + ':5000/1')
                        qr.make(fit=True)
                        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
                        b_channel, g_channel, r_channel = cv2.split(np.array(img))

                        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  #creating a dummy alpha channel image.

                        img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
                        icode= cv2.resize(img_BGRA,(200,200))

                        img_prev= self.addImage(img_prev,icode,(500,240))


                    count_down -=1
            else:
                if preview_on:
                    img_prev= self.addImage(img_prev,img_button,(250,230))

            cv2.imshow(WINDOW_NAME, img_prev)


            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
            if key == ord("r"):
                pass
            if key == ord("0"):
                pass

        # close any open windows
        cv2.destroyAllWindows()
        os.system("unclutter -idle 1 &")



app = Flask(__name__)
game = CameraPB()

@app.route('/')
def get_updates():
    return "<p>Hello, World!</p>"

@app.route('/1')
def get_image():
    filename = '/home/pi/PhotoBooth/image.jpg'

    return send_file(filename, mimetype='image/jpg')

@app.route('/2')
def starting():
    global start
    start=True

    return "<p>Starting!</p>"

@app.route('/3')
def changing():
    global bg_choose
    if bg_choose == 0:
        bg_choose =1
    else:
        bg_choose = 0

    return "<p>Changed!</p>"


# def take_pictureW():
#     print ("[INFO] Taking picture W")
#     # Replace the below path with the absolute or relative path to your CameraControlCmd executable.
#     camera_control_cmd_path = 'C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe'
#     test_camera = Camera(control_cmd_location=camera_control_cmd_path,collection_name="testing",save_folder="D:\\output\\")
#     test_camera.capture_single_image(autofocus=True)
# 
#     return

if __name__ == '__main__':
    #os.system("unclutter -idle 0 &")
    os.system('gio mount -s gphoto2')
    #os.system('python3 -m http.server 8080 &')

    game.start()
    app.run(port=5000, host='0.0.0.0', debug=False, use_reloader=False)
