

from max30102 import MAX30102
import hrcalc
import threading
import time
import numpy as np
import time


class HeartRateMonitor(object):
    """
    A class that encapsulates the max30102 device into a thread
    """

    LOOP_TIME = 0.01

    def __init__(self, print_raw=False, print_result=False):
        self.bpm = 0
        if print_raw is True:
            print('IR, Red')
        self.print_raw = print_raw
        self.print_result = print_result

    def run_sensor(self):
        sensor = MAX30102()
        ir_data = []
        red_data = []
        bpms = []
        self.Array_BPM = []
        self.Array_SPO = []
        self.tic = time.perf_counter()
        # run until told to stop
        while not self._thread.stopped:
            # check if any data is available
            num_bytes = sensor.get_data_present()
            if num_bytes > 0:
                # grab all the data and stash it into arrays
                while num_bytes > 0:
                    red, ir = sensor.read_fifo()
                    num_bytes -= 1
                    ir_data.append(ir)
                    red_data.append(red)
                    if self.print_raw:
                        print("VALUE : {0}, {1}".format(ir, red))

                while len(ir_data) > 100:
                    ir_data.pop(0)
                    red_data.pop(0)
                
                if len(ir_data) == 100:
                    bpm, valid_bpm, spo2, valid_spo2 = hrcalc.calc_hr_and_spo2(ir_data, red_data)
                    #if valid_bpm and valid_spo2 :
                    if 1 == 1 :
                        bpms.append(bpm)
                        while len(bpms) > 4:
                            bpms.pop(0)
                        self.bpm = np.mean(bpms)
                        if (np.mean(ir_data) < 50000 and np.mean(red_data) < 50000):
                            self.bpm = 0
                            if self.print_result:
                                print("Finger not detected")
                        if self.print_result:
                            print("BPM: {0}, SpO2: {1}".format(self.bpm, spo2))
                            self.bpm_value = self.bpm
                            self.spo2_value = spo2
                            print("EGG's BPM :", self.bpm_value, self.spo2_value )
                            
                            self.Array_BPM.append(self.bpm_value)
                            self.Arr_len = len(self.Array_BPM)
                            self.Array_SPO.append(self.spo2_value)
                            self.spo_len = len(self.Array_SPO)
                            #print(self.Array_BPM)

                    #print(self.Array_BPM)
            time.sleep(self.LOOP_TIME)
        print("Array ",self.Array_BPM)
        print("Length ",self.Arr_len)
        print("Array SPO ",self.Array_SPO)
        print("Length ",self.spo_len)
        sum_bpm = sum(self.Array_BPM)
        self.avg_bpm = sum_bpm / self.Arr_len

        sum_spo = sum(self.Array_SPO)
        self.avg_spo = sum_spo / self.spo_len

        print("avg : ", self.avg_bpm)
        print("spo's avg : ",self.avg_spo)
        
        self.toc = time.perf_counter()
        print(f"Duration {self.toc - self.tic:0.4f} seconds")
        
        sensor.shutdown()
        #return self.avg_bpm, self.avg_spo 

    def start_sensor(self):
        self._thread = threading.Thread(target=self.run_sensor)
        self._thread.stopped = False
        self._thread.start()

    def stop_sensor(self, timeout=2.0):
        self._thread.stopped = True
        self.bpm = 0
        self._thread.join(timeout)
