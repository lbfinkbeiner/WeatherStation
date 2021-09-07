"""
    File name: weather_report.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 9/5/2021
    Python version: 3.7.3
"""

import threading
import time as t
from pathlib import Path
from datetime import datetime as dt
import numpy as np, pandas as pd
import feed_interpreter, telnet_receiver, weather_gui
import shared as s

def load_data():
    """
    TODO: use some kind of Python os or sys or whatever library
        to look before you leap. Try catch statements
        seem like poor style if you have a better way of pre-checking
        the existence of today's files.
    """
    f1, f2 = s.current_records(mode='r')

    print("Prefixes retrieved")
    t.sleep(5)

    # 'round_trip' forces pandas to take its time transcribing
    # the values. The price is time, but we only expect to load once.
    s.df1 = pd.read_csv(f1, index_col=0, float_precision='round_trip')
    s.df2 = pd.read_csv(f2, index_col=0, float_precision='round_trip')

    print("Files read")
    t.sleep(5)

    # WARNING! THIS NEXT SECTION IS EXCLUSIVELY
    # INTENENDED FOR TESTING
    s.save_to_disk()
    print("Files saved")

def main():
    load_data()
    return

    # the thread numbering is entirely arbitrary
    t0 = threading.Thread(
        target=telnet_receiver.receive_from_ws1
    )
    t0.start()
    
    t1 = threading.Thread(
        target=telnet_receiver.receive_from_ws2
    )
    t1.start()
    
    t2 = threading.Thread(
        target=feed_interpreter.listen
    )
    t2.start()
   
    # TKInter does not play nicely with threading,
    # so the GUI gets to sit in the main routine.
    weather_gui.start()

main()

