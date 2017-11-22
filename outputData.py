import argparse
import math
import serial

import re
import threading
import sys

import numpy as np

from Config import config

import SupportVectorMachine as svm
from Config import Calibrate

import oscSend
from Config import keyInput

def serial_loop():
    with serial.Serial('COM5', 9600, timeout=0.1) as ser:
        setPortCount = 0

        is_loop = True

        between_a_and_a = False
        want_predict_num_array_raw = []
        arranged_sensor_date_list = []
        count_label = 0
        machine = svm.setup()
        if not is_loop:
            return
        try:
            while True:
                s = ser.readline()
                m = None

                if setPortCount < 100:
                    print("waiting port now" + str(setPortCount))
                    ser.write(bytes(str(2), 'UTF-8'))

                try:
                    de = s.decode('utf-8')
                    m = re.match("\-*[\w]+", str(de))
                except Exception as e:
                    pass
                if not m is None:
                    num = m.group()
                    setPortCount = setPortCount + 1
                    if num == "a":

                        between_a_and_a = True
                        count_label = 0
                        want_predict_num_array_raw = []
                    elif between_a_and_a:
                        if int(num) == 0:
                            print("重篤なエラーがあります")
                        want_predict_num_array_raw.append(int(num))

                    if len(want_predict_num_array_raw) == config.sensor_nums:
                        count_label = 0
                        if config.calibration_numbers is not None:
                            want_predict_num_array = want_predict_num_array_raw - config.calibration_numbers
                        else:
                            want_predict_num_array = want_predict_num_array_raw
                        config.is_calibration = Calibrate.start_calibration(config.is_calibration, want_predict_num_array)
                        while len(arranged_sensor_date_list) > 1:
                            arranged_sensor_date_list.pop(0)
                        arranged_sensor_date_list.append(want_predict_num_array)
                        want_predict_num_array = []
                        between_a_and_a = False
                        ser.flushInput()

                        predict = svm.stream(machine, np.array(arranged_sensor_date_list).astype(np.int64))
                        '''
                        if oscSend.osc_type == "r":
                            oscSend.send_raw(predict)
                        elif oscSend.osc_type == "f":
                            oscSend.send_face()
                        else:
                            pass
                        '''
                else:
                    pass
        except:
             print("Unexpected error:", sys.exc_info()[0])
             raise
        ser.close()

ser_loop = threading.Thread(target=serial_loop,name="ser_loop",args=())
ser_loop.setDaemon(True)
ser_loop.start()

def main():
    keyInput.key_input()


if __name__ == "__main__":
    main()
