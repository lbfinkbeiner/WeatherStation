"""
    File name: weather_report.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 9/7/2021
    Python version: 3.7.3
"""

import threading
import time as t
from pathlib import Path
from datetime import datetime as dt
import numpy as np, pandas as pd
import feed_interpreter, telnet_receiver, weather_gui
import shared as s

import traceback
import logging
import logging.handlers
import os

def load_data():
    """
    TODO: use some kind of Python os or sys or whatever library
        to look before you leap. Try catch statements
        seem like poor style if you have a better way of pre-checking
        the existence of today's files.
    """
    try:
        f1, f2 = s.current_records(mode='r')
    except FileNotFoundError:
        print("No pre-existing records found using today's date. Starting a new file.")
        return

    # 'round_trip' forces pandas to take its time transcribing
    # the values. The price is time, but we only expect to load once.
    s.df1 = pd.read_csv(f1, index_col=0, float_precision='round_trip')
    s.df2 = pd.read_csv(f2, index_col=0, float_precision='round_trip')

    print("Pre-existing records checked.")

def spawn_workers():
    logging.info(str(int(t.time())) + ": spawn_workers routine initiated.")
    s.initialize_dfs()
    load_data()

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

def main():
    try:
        s.root_log = logging.getLogger()
        s.root_log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
        s.log_formatter = logging.Formatter(logging.BASIC_FORMAT)
        s.initialize_logger()

        spawn_workers()
    except Exception as e:
        logging.error(str(int(t.time())) + ": " + traceback.format_exc())

main()

