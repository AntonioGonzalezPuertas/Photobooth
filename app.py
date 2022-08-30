import threading
import time
from flask import Flask, render_template, send_file
import cv2

class myGame(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.board = 1

    def run(self):
        print('Bingo')
        while True:
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
        pass


app = Flask(__name__)
game = myGame()

@app.route('/')
def get_updates():
    return "<p>Hello, World!</p>"

@app.route('/1')
def get_image():
    filename = 'capture_0.jpg'

    return send_file(filename, mimetype='image/jpg')

if __name__ == "__main__":
    cv2.namedWindow('test',cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('test', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    game.start()
    app.run(port=5000, host='0.0.0.0', debug=False, use_reloader=False)
