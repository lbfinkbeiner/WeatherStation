"""
    File name: weather_report.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 9/5/2021
    Python version: 3.7.3
"""

import threading
import feed_interpreter, telnet_receiver, weather_gui
import numpy as np, pandas as pd

"""
'soul' is just jargon I made up to describe a function
that updates a specific label on the GUI. Without
this strange work-around those functions are
entirely internal and difficult to see from here.
"""
feed1 = {"raw": "", "updated": False,
         "primary_soul": None, "comm_soul": None}
feed2 = {"raw": "", "updated": False,
         "primary_soul": None, "comm_soul": None}

full_feed = {
    "feed1": feed1,
    "feed2": feed2,
    "diff_soul": None,
    "graph_soul": None,
    "graph_data": {
        "Ta": {
            "x": None,
            "y": None
        }
    }
}

var_abbrs = [
    "Dn",
    "Dm",
    "Dx",
    "Sn",
    "Sm",
    "Sx",
    "Ta",
    "Ua",
    "Pa",
    "Rc",
    "Rd",
    "Ri",
    "Hc",
    "Hd",
    "Hi",
    "Rp",
    "Hp",
    "Th",
    "Vh",
    "Vs",
    "Vr"
]

df_columns = 

df1 = pd.DataFrame(columns=var_abbrs)
df2 = pd.DataFrame(columns=var_abbrs)

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
        args=(full_feed, df1, df2,)
    )
    t2.start()
    
    t3 = threading.Thread(
        target=weather_gui.start,
        args=(full_feed, df1, df2,)
    )
    t3.start()

main()
