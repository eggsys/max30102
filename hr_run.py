from heartrate_monitor import HeartRateMonitor
import time
import argparse
class get_max30102(object) :
    
        
    def __init__(self):
        print("ok go")
        self.get_hr()

    def get_hr(self):    
        parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
        parser.add_argument("-r", "--raw", action="store_true",
                            help="print raw data instead of calculation result")
        parser.add_argument("-t", "--time", type=int, default=15,
                            help="duration in seconds to read from sensor, default 30")
        args = parser.parse_args()

        print('sensor starting...')
        hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))
        hrm.start_sensor()
        try:
            time.sleep(args.time)
        except KeyboardInterrupt:
            print('keyboard interrupt detected, exiting...')

        hrm.stop_sensor()
        print('sensor stoped!')
        self.avg_spo = hrm.avg_spo
        self.avg_bpm = hrm.avg_bpm
        print("######## MAIN ##########")
        print(hrm.avg_bpm, hrm.avg_spo)
        print("######## MAIN ##########")
