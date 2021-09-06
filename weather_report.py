"""
    File name: weather_report.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 9/5/2021
    Python version: 3.7.3
"""

import threading
import numpy as np, pandas as pd
import feed_interpreter, telnet_receiver, weather_gui

def main():
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
    
    t3 = threading.Thread(
        target=weather_gui.start
    )
    t3.start()

    print("We did in fact reach the end of the main routine.")

main()

