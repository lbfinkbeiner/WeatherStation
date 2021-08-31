"""
    File name: weather_report.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 8/30/2021
    Python version: 3.7.3
"""

import threading
import telnet_interpret, telnet_receiver

feed = {"raw_output": "", "changed": False}

# Credit to Santa on Stackflow for the following function
def main():
    tasks = [telnet_interpret.report, telnet_receiver.receive]
    for task in tasks:
        t = threading.Thread(target=task, args=(feed,))
        t.start()
        
main()
