import cv2
import os
import time
import numpy as np
import datetime
import gphoto2 as gp

#from DigiCam.Camera import Camera
#import winsound

""" ///////// CONSTANTS ///////// """

if os.name == 'nt':
    FORMAT_DIR = '\\' # Windows
    is_windows = True
else:
    FORMAT_DIR = '/' # Linux
    is_windows = False

WINDOW_NAME = 'Photo Booth'

# button dimensions (y1,y2,x1,x2)
button_pos = [0,0,0,0]
start = False
"""///////////////////////////////"""






def take_pictureW():
    print ("[INFO] Taking picture W")
    # Replace the below path with the absolute or relative path to your CameraControlCmd executable.
    camera_control_cmd_path = 'C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe'
    test_camera = Camera(control_cmd_location=camera_control_cmd_path,collection_name="testing",save_folder="D:\\output\\")
    test_camera.capture_single_image(autofocus=True)

    return

def take_picture():
    print ("[INFO] Taking picture")
    camera = gp.Camera()
    camera.init()
    
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
    target = os.path.join(os.getcwd(), "capture_0.jpg")
    print('Copying image to', target)
    camera_file = camera.file_get(
        file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)
    camera.exit()
    #img = cv2.imread('testing_0.jpg')
     #cv2.imshow('image',img)



def loop():
    global start
    countdown = 4

    while True:

        if start:
            if countdown >= 0:
                print(countdown)
                background= cv2.imread('background.png',-1)
                showText(background,str(countdown),(300,280))
                countdown -=1
                time.sleep(1)
            else:
                if is_windows:
                    take_pictureW()
                else:
                    take_picture()
                background= cv2.imread('background.png',-1)
                target = os.path.join(os.getcwd(), "capture_0.jpg")
                img= cv2.imread(target,-1)
                b_channel, g_channel, r_channel = cv2.split(img)

                alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  #creating a dummy alpha channel image.

                img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
                print((background.shape[0],background.shape[1]))
                i= cv2.resize(img_BGRA,(int(background.shape[1]/2),int(background.shape[0]/2)))
                posx=int(background.shape[1]/2 - background.shape[1]/4)
                posy=int(background.shape[0]/2 - background.shape[0]/4)
                showImage(background,i,(posx,posy))
                start=False
                countdown=5

            if countdown == -1:

                t= cv2.imread('background.png',-1)
                white_background = np.zeros([t.shape[0],t.shape[1],1],dtype=np.uint8)
                white_background.fill(255)
                cv2.imshow(WINDOW_NAME,white_background)



        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        if key == ord("r"):
            pass
        if key == ord("p"):
            pass
        if key == ord("v"):
            pass
        if key == ord("d"):
            pass
        if key == ord("n"):
            pass

        if key == ord("0"):
            pass
        if key == ord("1"):
            pass
        if key == ord("2"):
            pass
        if key == ord("3"):
            pass
        if key == ord("4"):
            pass


def showImage(background,image,pos=(0,0)):
    #get position and crop pasting area if needed
    y = pos[0]
    x = pos[1]
    bgWidth = background.shape[0]
    bgHeight = background.shape[1]
    frWidth = image.shape[0]
    frHeight = image.shape[1]
    width = bgWidth-x
    height = bgHeight-y
    if frWidth<width:
        width = frWidth
    if frHeight<height:
        height = frHeight
    # normalize alpha channels from 0-255 to 0-1
    alpha_background = background[x:x+width,y:y+height,3] / 255.0
    alpha_foreground = image[:width,:height,3] / 255.0
    # set adjusted colors
    for color in range(0, 3):
        fr = alpha_foreground * image[:width,:height,color]
        bg = alpha_background * background[x:x+width,y:y+height,color] * (1 - alpha_foreground)
        background[x:x+width,y:y+height,color] = fr+bg
    # set adjusted alpha and denormalize back to 0-255
    background[x:x+width,y:y+height,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255
    cv2.imshow(WINDOW_NAME, background)

def showText(background,text,pos=(0,0)):
    #get position and crop pasting area if needed
    x = pos[0]
    y = pos[1]
    bgWidth = background.shape[0]
    bgHeight = background.shape[1]


    cv2.putText(background,text,org=(x,y), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale= 8,color=(255,255,255))
    cv2.imshow(WINDOW_NAME, background)



# function that handles the mousclicks
def process_click(event, x, y,flags, params):
    global button_pos, start
    # check if the click is within the dimensions of the button
    if event == cv2.EVENT_LBUTTONDOWN:
        if x > button_pos[0] and y > button_pos[1] and x < button_pos[2] and y < button_pos[3]:
            start=True


def main():
    global button_pos
    print("[INFO] Running PhotoBooth")


    

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_FULLSCREEN)
    cv2.setWindowTitle(WINDOW_NAME, WINDOW_NAME)

    background= cv2.imread('background.png',-1)
    bg_height, bg_width, _ = background.shape

    img= cv2.imread('start_button.png',-1)
    img_height, img_width, _ = img.shape

    offset =(280,80)

    showImage(background,img,(offset[0],offset[1]))
    button_pos = [offset[0], offset[1],offset[0]+img_width,offset[1]+img_height]



    cv2.setMouseCallback(WINDOW_NAME, process_click)


    loop()

    # close any open windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
