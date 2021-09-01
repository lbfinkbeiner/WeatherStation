"""
    File name: weather_report.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 8/31/2021
    Python version: 3.7.3
"""

import threading
import feed_interpreter, telnet_receiver, weather_gui

#! We may want to add more fields and take some steps back.
# For example, the 'styled' fields aggregate all text output.
# But the weather_gui needs some numbers with which to work,
# for example to build the plots...
feed1 = {"raw": "", "updated": False,
         "styled": "", "soul": None}
feed2 = {"raw": "", "updated": False,
         "styled": "", "soul": None}

full_feed = {"feed1": feed1, "feed2": feed2}

def main():
    # the thread numbering is entirely arbitrary
    t0 = threading.Thread(target=telnet_receiver.receive_from_ws1, args=(feed1,))
    t0.start()
    
    t1 = threading.Thread(target=telnet_receiver.receive_from_ws2, args=(feed2,))
    t1.start()
    
    t2 = threading.Thread(target=feed_interpreter.listen, args=(full_feed,))
    t2.start()
    
    t3 = threading.Thread(target=weather_gui.start, args=(full_feed,))
    t3.start()

main()
