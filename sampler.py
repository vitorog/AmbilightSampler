import cv2
from numpy import median
from time import time

class Sampler:
    num_side_leds = 0
    num_top_leds = 0
    num_bottom_leds = 0

    """Size of the ROI from where colors will be sampled."""
    sample_roi_size = 100

    def __init__(self):
        print("Initializing sampler")

    def sample_from_webcam(self):
        cap = cv2.VideoCapture(0)

        test = cap.get(cv2.CAP_PROP_POS_MSEC)
        ratio = cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
        contrast = cap.get(cv2.CAP_PROP_CONTRAST)
        saturation = cap.get(cv2.CAP_PROP_SATURATION)
        hue = cap.get(cv2.CAP_PROP_HUE)
        gain = cap.get(cv2.CAP_PROP_GAIN)
        exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
        print("Test: ", test)
        print("Ratio: ", ratio)
        print("Frame Rate: ", frame_rate)
        print("Height: ", height)
        print("Width: ", width)
        print("Brightness: ", brightness)
        print("Contrast: ", contrast)
        print("Saturation: ", saturation)
        print("Hue: ", hue)
        print("Gain: ", gain)
        print("Exposure: ", exposure)

        while True:
            s, im = cap.read()
            cv2.imshow("Webcam", im)
            cv2.waitKey(1)

    def sample_from_image(self, img):
        # rols, cols, channels
        height, width, channels = img.shape
        print('Img is: ' + str(width) + ' x ' + str(height))

        start = time()

        end = time()

        elapsed = end - start
        print(elapsed)

if __name__ == '__main__':
    s = Sampler()
    img = cv2.imread('big_buck_bunny.jpg')
    img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    s.sample_from_image(img)