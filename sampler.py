import cv2
from numpy import median
import time
from math import floor
import serial
import struct
from WebcamVideoStream import WebcamVideoStream

class Sampler:
    num_side_leds = 38
    num_top_leds = 65
    num_bottom_leds = 68
    roi_size = 100

    left_leds_colors = []
    right_leds_colors = []
    top_leds_colors = []
    bottom_led_colors = []

    """Size of the ROI from where colors will be sampled."""
    sample_roi_size = 100

    def __init__(self):
        print("Initializing sampler")

    def sample_from_webcam(self):
        # cap = cv2.VideoCapture(0)
        vs = WebcamVideoStream(src=0).start()

        # test = cap.get(cv2.CAP_PROP_POS_MSEC)
        # ratio = cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
        # frame_rate = cap.get(cv2.CAP_PROP_FPS)
        # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
        # contrast = cap.get(cv2.CAP_PROP_CONTRAST)
        # saturation = cap.get(cv2.CAP_PROP_SATURATION)
        # hue = cap.get(cv2.CAP_PROP_HUE)
        # gain = cap.get(cv2.CAP_PROP_GAIN)
        # exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        # cap.set(cv2.CAP_PROP_EXPOSURE, -6.0)
        # cap.set(cv2.CAP_PROP_FPS, 30)
        # cap.set(cv2.CAP_PROP_GAIN, 0)
        # cap.set(cv2.CAP_PROP_BRIGHTNESS, 64)
        # cap.set(cv2.CAP_PROP_CONTRAST, 64)
        # cap.set(cv2.CAP_PROP_SATURATION, 64)
        # print("Test: ", test)
        # print("Ratio: ", ratio)
        # print("Frame Rate: ", frame_rate)
        # print("Height: ", height)
        # print("Width: ", width)
        # print("Brightness: ", brightness)
        # print("Contrast: ", contrast)
        # print("Saturation: ", saturation)
        # print("Hue: ", hue)
        # print("Gain: ", gain)
        # print("Exposure: ", exposure)

        arduino = serial.Serial('COM3', 1000000, timeout=.1)
        time.sleep(1)
        arduino.write('r'.encode())
        time.sleep(1)

        # arduino.write("Hello from Python".encode())
        # img = cv2.imread('red.png')
        while True:
            start = time.time()

            #s, img = cap.read()
            img = vs.read()
            #cv2.resize(img, None, 0.5, 0.5, cv2.INTER_LINEAR)
            self.sample_from_image(img)

            colors = []
            for color in self.left_leds_colors:
                colors.append(int(color[2]))
                colors.append(int(color[1]))
                colors.append(int(color[0]))

            for color in self.top_leds_colors:
                colors.append(int(color[2]))
                colors.append(int(color[1]))
                colors.append(int(color[0]))

            for color in self.right_leds_colors:
                colors.append(int(color[2]))
                colors.append(int(color[1]))
                colors.append(int(color[0]))

            for color in self.bottom_led_colors:
                colors.append(int(color[2]))
                colors.append(int(color[1]))
                colors.append(int(color[0]))

            bytes = struct.pack('c' + ('B' * len(colors)) + 'c', '@'.encode(), *colors, '#'.encode())
            arduino.write(bytes)

            img_with_borders = self.show_image_with_colors(img)

            # cv2.imshow("Image with Borders", img_with_borders)
            # cv2.waitKey(30)
            # time.sleep(0.1)

            end = time.time()
            elapsed = end - start
            print(str(1 / elapsed) + " FPS")

    def sample_from_image(self, img):
        # rols, cols, channels
        # print('Img is: ' + str(width) + ' x ' + str(height))
        self.process_side_borders(img)
        self.process_top_border(img)
        self.process_bottom_border(img)

    def show_image_with_colors(self, img):
        img_with_borders = cv2.copyMakeBorder(img, self.roi_size, self.roi_size, self.roi_size, self.roi_size,
                                              cv2.BORDER_CONSTANT, value=[0, 0, 0])

        height, width, channels = img.shape
        vertical_size_roi = round(height / self.num_side_leds)

        for i in range(self.num_side_leds):
            y_start_pos = self.roi_size + i * vertical_size_roi
            y_end_pos = y_start_pos + vertical_size_roi

            if i == self.num_side_leds - 1:
                y_end_pos = self.roi_size + height

            img_with_borders[y_start_pos:y_end_pos, 0:self.roi_size] = self.left_leds_colors[i]
            img_with_borders[y_start_pos:y_end_pos, width+self.roi_size:width+2*self.roi_size] = self.right_leds_colors[i]

        horizontal_size_roi = floor(width / self.num_top_leds)
        for i in range(self.num_top_leds):
            x_start_pos = self.roi_size + i * horizontal_size_roi
            x_end_pos = x_start_pos + horizontal_size_roi

            if i == self.num_top_leds - 1:
                x_end_pos = self.roi_size + width

            img_with_borders[0:self.roi_size, x_start_pos:x_end_pos] = self.top_leds_colors[i]

        for i in range(self.num_bottom_leds):
            x_start_pos = self.roi_size + i * horizontal_size_roi
            x_end_pos = x_start_pos + horizontal_size_roi

            if i == self.num_top_leds - 1:
                x_end_pos = self.roi_size + width

            img_with_borders[height+self.roi_size:height+2*self.roi_size, x_start_pos:x_end_pos] = self.bottom_led_colors[i]

        return img_with_borders

    def process_top_border(self, img):
        height, width, channels = img.shape

        horizontal_size_roi = floor(width / self.num_top_leds)

        self.top_leds_colors = []

        for i in range(self.num_top_leds):
            x_start_pos = i * horizontal_size_roi
            x_end_pos = x_start_pos + horizontal_size_roi

            if i == self.num_top_leds - 1:
                x_end_pos = width

            top_roi = img[0:self.roi_size, x_start_pos:x_end_pos]
            b, g, r = cv2.split(top_roi)
            self.top_leds_colors.append([median(b), median(g), median(r)])

    def process_bottom_border(self, img):
        height, width, channels = img.shape

        horizontal_size_roi = floor(width / self.num_bottom_leds)

        self.bottom_led_colors = []

        for i in range(self.num_bottom_leds):
            x_start_pos = i * horizontal_size_roi
            x_end_pos = x_start_pos + horizontal_size_roi

            if i == self.num_top_leds - 1:
                x_end_pos = width

            top_roi = img[height-self.roi_size:height, x_start_pos:x_end_pos]
            b, g, r = cv2.split(top_roi)
            self.bottom_led_colors.append([median(b), median(g), median(r)])

    def process_side_borders(self, img):
        height, width, channels = img.shape

        vertical_size_roi = floor(height / self.num_side_leds)

        self.left_leds_colors = []
        self.right_leds_colors = []

        for i in range(self.num_side_leds):
            y_start_pos = i*vertical_size_roi
            y_end_pos = y_start_pos + vertical_size_roi

            if i == self.num_side_leds - 1:
                y_end_pos = height

            left_roi = img[y_start_pos:y_end_pos, 0:self.roi_size]
            b,g,r = cv2.split(left_roi)
            self.left_leds_colors.append([median(b), median(g), median(r)])

            right_roi = img[y_start_pos:y_end_pos, width-self.roi_size:width]
            b, g, r = cv2.split(right_roi)
            self.right_leds_colors.append([median(b), median(g), median(r)])



if __name__ == '__main__':
    s = Sampler()
    s.sample_from_webcam()
    # arduino = serial.Serial('COM3', 1000000, timeout=.1)
    # time.sleep(1)
    # #
    # arduino.write('r'.encode())
    # #
    # time.sleep(2)
    # #
    # # count = 0
    #
    # while True:
    #     colors = []
    #     for x in range(209):
    #         colors.append(255)
    #         colors.append(0)
    #         colors.append(0)
    #     # s = bytes('@' + chr(255) + chr(0) + chr(0) + '#', "utf-8")
    #     # print(s)
    #     # arduino.write(s)
    #     test = struct.pack('c' + 'B' * len(colors) + 'c', '@'.encode(), *colors, '#'.encode())
    #     arduino.write(test)
    #
    #     # data = arduino.readline()
    #     # if data:
    #     #     print(data.decode())
    #     time.sleep(1)
    #
    #     colors = []
    #     for x in range(209):
    #         colors.append(0)
    #         colors.append(255)
    #         colors.append(0)
    #     # s = bytes('@' + chr(255) + chr(0) + chr(0) + '#', "utf-8")
    #     # print(s)
    #     # arduino.write(s)
    #     test = struct.pack('c' + 'B' * len(colors) + 'c', '@'.encode(), *colors, '#'.encode())
    #     arduino.write(test)
    #
    #     time.sleep(1)
    #
    #     colors = []
    #     for x in range(209):
    #         colors.append(0)
    #         colors.append(0)
    #         colors.append(255)
    #     # s = bytes('@' + chr(255) + chr(0) + chr(0) + '#', "utf-8")
    #     # print(s)
    #     # arduino.write(s)
    #     test = struct.pack('c' + 'B' * len(colors) + 'c', '@'.encode(), *colors, '#'.encode())
    #     arduino.write(test)
    #
    #     time.sleep(1)


    #         print(i)
    #         arduino.write("@".encode())
    #         if count == 0:
    #             arduino.write(struct.pack('>BBBB', i, int(0), int(0), int(255)))
    #         else:
    #             arduino.write(struct.pack('>BBBB', i, int(255), int(0), int(0)))
    #         arduino.write('#'.encode())
    #         # data = arduino.readline()
    #         # if data:
    #         #     print(data.decode())
    #     arduino.write('$'.encode())
    #     time.sleep(0.1)
    #     count = 1


