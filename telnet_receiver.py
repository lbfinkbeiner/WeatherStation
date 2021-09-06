"""
    File name: telnet_receiver.py
    Author: Lukas Finkbeiner
    Date created: 8/30/2021
    Date last modified: 9/5/2021
    Python version: 3.7.3
"""

HOST_WS1 = 'weatherport-primary.hcro.org'
PORT_WS1 = 4001

HOST_WS2 = 'weatherport-secondary.hcro.org'
PORT_WS2 = 4001

from telnetlib import Telnet
import re
import time as t
import shared as s

# This pattern indicates the end of a full transmission (one full set of variable values)
batch_terminator = "Vr=\d+\.\d+V"

def receive(feed, HOST, PORT):
    with Telnet(HOST, PORT) as tn:
        latest = ""
        while not s.shutting_down:
            next_byte = tn.read_eager()
            try:
                next_char = next_byte.decode("ascii")
                
                latest += next_char
                terminator_match = re.search(batch_terminator, latest)

                if terminator_match is not None:
                    terminator = terminator_match.group(0)
                    terminator_start_i = latest.find(terminator)
                    terminator_end_i = terminator_start_i + len(terminator)

                    feed["raw"] = latest[:terminator_end_i]
                    # publish the change
                    feed["latest_index"] = t.time()
                    feed["updated"] = True
                    latest = ""
            except UnicodeDecodeError:
                # I am not really sure what I should do
                # about this, if anything.
                latest = ""

# This section is a bit dumb, but we only have
# two weather stations, so it's easy and readable.
def receive_from_ws1():
    receive(s.feed1, HOST_WS1, PORT_WS1)

def receive_from_ws2():
    receive(s.feed2, HOST_WS2, PORT_WS2)

