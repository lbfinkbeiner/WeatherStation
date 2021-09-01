"""
    File name: weather_report.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 9/1/2021
    Python version: 3.7.3
"""

import threading
import feed_interpreter, telnet_receiver, weather_gui

"""
'soul' is just jargon I made up to describe a function
that updates a specific label on the GUI. Without
this strange work-around those functions are
entirely internal and difficult to see from here.
"""
feed1 = {"raw": "", "updated": False, "soul": None}
feed2 = {"raw": "", "updated": False, "soul": None}

full_feed = {"feed1": feed1, "feed2": feed2,
             "diff_soul": None, "comms_soul": None}

def main():
    # the thread numbering is entirely arbitrary
    t0 = threading.Thread(
        target=telnet_receiver.receive_from_ws1,
        args=(feed1,)
    )
    t0.start()
    
    t1 = threading.Thread(
        target=telnet_receiver.receive_from_ws2,
        args=(feed2,)
    )
    t1.start()
    
    t2 = threading.Thread(
        target=feed_interpreter.listen,
        args=(full_feed,)
    )
    t2.start()
    
    t3 = threading.Thread(
        target=weather_gui.start,
        args=(full_feed,)
    )
    t3.start()

main()
